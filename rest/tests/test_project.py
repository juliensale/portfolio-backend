import os
from PIL import Image
from tempfile import NamedTemporaryFile
from django.test import TestCase
from core.models import Project, Review
from rest.serializers import ProjectSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

PROJECT_URL = reverse('rest:project-list')


class ProjectApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.credentials(
            HTTP_AUTHORIZATION='Token ' + os.environ['ADMIN_TOKEN'])

    def test_retrieve_projects(self):
        """Tests retrieving projects"""
        Project.objects.create(
            name={"en": "Test project 1", "fr": "Test project 1"},
            description={"en": ["Test desc"], "fr": ["Test desc"]}
        )
        Project.objects.create(
            name={"en": "Test project 2", "fr": "Test project 2"},
            description={"en": ["Test desc"], "fr": ["Test desc"]}
        )

        res = self.client.get(PROJECT_URL)
        projects = Project.objects.all().order_by('name')
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['name'], serializer.data[0]['name'])

    def test_list_fields(self):
        """Test that only some fields are visible in the list view"""
        Project.objects.create(
            name={"en": "Test project", "fr": "Projet test"},
            description={"en": ["Test desc"], "fr": ["Test desc"]}
        )

        res = self.client.get(PROJECT_URL)

        has_good_attributes = ('id' in res.data[0]
                               and 'name' in res.data[0]
                               and 'description' in res.data[0]
                               and 'image' in res.data[0]
                               and 'technologies' in res.data[0]
                               and 'github' not in res.data[0]
                               and 'link' not in res.data[0]
                               and 'client' not in res.data[0]
                               and 'duration' not in res.data[0]
                               )
        self.assertTrue(has_good_attributes)

    def test_detail_fields(self):
        """Test that all the fields are visibile in the details view"""
        project = Project.objects.create(
            name={"en": "Test project", "fr": "Projet test"},
            description={"en": ["Test desc"], "fr": ["Test desc"]}
        )

        detail_url = reverse('rest:project-detail', kwargs={"pk": project.id})
        res = self.client.get(detail_url)

        has_good_attributes = ('id' in res.data
                               and 'name' in res.data
                               and 'description' in res.data
                               and 'image' in res.data
                               and 'technologies' in res.data
                               and 'github' in res.data
                               and 'link' in res.data
                               and 'client' in res.data
                               and 'duration' in res.data
                               )
        self.assertTrue(has_good_attributes)

    def test_create_admin_only(self):
        """Tests that the creation requires admin rights"""
        payload = {
            "name": {"en": "Test project", "fr": "Projet test"},
            "description": {"en": ["Test desc"], "fr": ["Test desc"]}
        }
        res = self.client.post(PROJECT_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_project(self):
        """Tests creating a project"""
        payload = {
            "name": {"en": "Test project", "fr": "Projet test"},
            "description": {"en": ["Test desc"], "fr": ["Test desc"]}
        }
        res = self.admin_client.post(
            PROJECT_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Project.objects.all().filter(
            name=payload['name']).exists()
        self.assertTrue(exists)
        Project.objects.all().filter(name=payload['name']).delete()

    def test_create_project_wrong_credentials(self):
        """Tests creating a project with wrong credentials fails"""
        payload = {
            "name": {"en": [1, 2, 3], "fr": "Projet test"},
            "description": {"en": ["Test desc"], "fr": ["Test desc"]}
        }
        res = self.admin_client.post(
            PROJECT_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_admin_only(self):
        """Tests that the update requires admin rights"""
        project = Project.objects.create(
            name={"en": "Test project", "fr": "Projet test"},
            description={"en": ["Test desc"], "fr": ["Test desc"]}
        )
        payload = {"name": {"en": "New name", "fr": "Nouveau nom"}}
        detail_url = reverse('rest:project-detail', kwargs={'pk': project.id})
        res = self.client.patch(detail_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_project(self):
        """Tests updating a project"""
        project = Project.objects.create(
            name={"en": "Test project", "fr": "Projet test"},
            description={"en": ["Test desc"], "fr": ["Test desc"]}
        )
        payload = {"name": {"en": "New name", "fr": "Nouveau nom"}}
        detail_url = reverse('rest:project-detail', kwargs={'pk': project.id})
        res = self.admin_client.patch(detail_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        project.refresh_from_db()
        self.assertEqual(project.name, payload['name'])

    def test_delete_admin_only(self):
        """Tests that the deletion requires admin rights"""
        name = {"en": "Test project", "fr": "Projet test"}
        project = Project.objects.create(
            name=name,
            description={"en": ["Test desc"], "fr": ["Test desc"]}
        )
        detail_url = reverse('rest:project-detail', kwargs={'pk': project.id})
        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        exists = Project.objects.all().filter(name=name).exists()
        self.assertTrue(exists)

    def test_delete_project(self):
        """Tests deleting a project"""
        name = {"en": "Test project", "fr": "Projet test"}
        project = Project.objects.create(
            name=name,
            description={"en": ["Test desc"], "fr": ["Test desc"]}
        )
        detail_url = reverse('rest:project-detail', kwargs={'pk': project.id})
        res = self.admin_client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Project.objects.all().filter(name=name).exists()
        self.assertFalse(exists)

    def test_get_project_review(self):
        """Test getting the review associated to a project"""
        project = Project.objects.create(
            name={"en": "Test project", "fr": "Projet test"},
            description={"en": ["test"], "fr": ["test"]}
        )
        associated_review = Review.objects.all().filter(project=project.id)[0]

        url = reverse('rest:project-review', kwargs={'pk': project.id})
        res = self.client.get(url)
        serializer = ReviewSerializer(associated_review)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class ProjectImageApiTests(TestCase):
    """Tests for the image publishing API"""

    def setUp(self):
        self.client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.credentials(
            HTTP_AUTHORIZATION='Token ' + os.environ['ADMIN_TOKEN'])

    def test_publish_image_admin_only(self):
        """Test that publishing an image requires admin rights"""
        with NamedTemporaryFile(suffix=".jpeg") as ntf:
            project = Project.objects.create(
                name={"en": "Test project", "fr": "Projet test"},
                description={"en": ["Test desc"], "fr": ["Test desc"]}
            )
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            detail_url = reverse('rest:project-upload-image',
                                 kwargs={'pk': project.id})
            res = self.client.post(detail_url, {"image": ntf})
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_publish_image(self):
        """Test publishing an image to a project"""
        with NamedTemporaryFile(suffix=".jpeg") as ntf:
            project = Project.objects.create(
                name={"en": "Test project", "fr": "Projet test"},
                description={"en": ["Test desc"], "fr": ["Test desc"]}
            )
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            detail_url = reverse('rest:project-upload-image',
                                 kwargs={'pk': project.id})
            res = self.admin_client.post(detail_url, {"image": ntf})
            self.assertEqual(res.status_code, status.HTTP_200_OK)
            project.refresh_from_db()
            project.delete()
