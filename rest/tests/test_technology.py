from PIL import Image
from tempfile import NamedTemporaryFile
from django.test import TestCase
from django.urls import reverse
from core.models import Technology
from rest.serializers import TechnologySerializer
from rest_framework.test import APIClient
from rest_framework import status
import os

TECHNOLOGY_URL = reverse('rest:technology-list')


class TechnologyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.credentials(
            HTTP_AUTHORIZATION='Token ' + os.environ['ADMIN_TOKEN'])

    def test_retrieve_technologies(self):
        """Test retrieving technologies"""
        Technology.objects.create(name='Test tech 1')
        Technology.objects.create(name='Test tech 2')

        res = self.client.get(TECHNOLOGY_URL)
        technologies = Technology.objects.all().order_by('name')
        serializer = TechnologySerializer(technologies, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'], serializer.data[0]['name'])
        self.assertEqual(len(res.data), 2)

    def test_create_admin_only(self):
        """Test that the creation requires the admin token"""
        with NamedTemporaryFile(suffix='.jpeg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)

            payload = {"name": "Test tech", "image": ntf}
            res = self.client.post(
                TECHNOLOGY_URL, payload, format='multipart')
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        """Test creating a technology"""
        with NamedTemporaryFile(suffix='.jpeg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)

            payload = {"name": "Test tech", "image": ntf}
            res = self.admin_client.post(
                TECHNOLOGY_URL, payload, format='multipart')
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            exists = Technology.objects.all().filter(
                name=payload['name']).exists()
            self.assertTrue(exists)
            Technology.objects.all().filter(
                name=payload['name'])[0].delete()

    def test_create_wrong_credentials(self):
        """Test creating a technology with wrong credentials fails"""
        payload = {"name": [1, 2, 3]}
        res = self.admin_client.post(TECHNOLOGY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_admin_only(self):
        """Test that the update requires the admin token"""
        technology = Technology.objects.create(name='Test tech')
        payload = {'name': 'New name'}
        detail_url = reverse(
            'rest:technology-detail',
            kwargs={'pk': technology.id}
        )
        res = self.client.patch(detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update(self):
        """Test updating a technology"""
        technology = Technology.objects.create(name='Test tech')
        payload = {'name': 'New name'}
        detail_url = reverse(
            'rest:technology-detail',
            kwargs={'pk': technology.id}
        )
        res = self.admin_client.patch(detail_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        technology.refresh_from_db()
        self.assertEqual(technology.name, payload['name'])

    def test_delete_admin_only(self):
        """Test that the deletion requires the admin token"""
        name = 'Test tech'
        technology = Technology.objects.create(name=name)
        detail_url = reverse(
            'rest:technology-detail',
            kwargs={'pk': technology.id}
        )
        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        exists = Technology.objects.all().filter(name=name).exists()
        self.assertTrue(exists)

    def test_delete(self):
        """Test deleting a technology"""
        name = 'Test tech'
        technology = Technology.objects.create(name=name)
        detail_url = reverse(
            'rest:technology-detail',
            kwargs={'pk': technology.id}
        )
        res = self.admin_client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Technology.objects.all().filter(name=name).exists()
        self.assertFalse(exists)
