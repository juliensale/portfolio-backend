import os
from django.test import TestCase
from django.urls import reverse
from core.models import Skill

from rest_framework.test import APIClient
from rest.serializers import SkillSerializer
from rest_framework import status

SKILL_URL = reverse('rest:skill-list')


class SkillApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.credentials(
            HTTP_AUTHORIZATION='Token ' + os.environ['ADMIN_TOKEN'])

    def test_retrieve_skills(self):
        """Test retrieving skills"""
        Skill.objects.create(
            date=[2, 2022],
            name={"en": "Test skill 1", "fr": "Skill de test 1"},
            description={
                "en": "Test desc",
                "fr": "Desc test"
            }
        )
        Skill.objects.create(
            date=[8, 2021],
            name={"en": "Test skill 2", "fr": "Skill de test 2"},
            description={
                "en": "Test desc",
                "fr": "Desc test"
            }
        )

        res = self.client.get(SKILL_URL)
        skills = Skill.objects.all().order_by('name')
        serializer = SkillSerializer(skills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['name'], serializer.data[0]['name'])

    def test_create_admin_only(self):
        """Test that the creation requires admin rights"""
        payload = {
            "date": [2, 2022],
            "name": {"en": "Test skill", "fr": "Skill de test"},
            "description": {"en": "Test desc", "fr": "Desc test"}
        }
        res = self.client.post(SKILL_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_skill(self):
        """Test creating a skill"""
        payload = {
            "date": [2, 2022],
            "name": {"en": "Test skill", "fr": "Skill de test"},
            "description": {"en": "Test desc", "fr": "Desc test"}
        }
        res = self.admin_client.post(SKILL_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Skill.objects.all().filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_skill_wrong_credentials(self):
        """Test creating a skill with wrong credentials fails"""
        payload = {
            "date": "22 august",
            "name": {"en": "Test skill", "fr": "Skill de test"},
            "description": {"en": "Test desc", "fr": "Desc test"}
        }
        res = self.admin_client.post(SKILL_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_admin_only(self):
        """Test that the update requires admin rights"""
        skill = Skill.objects.create(
            date=[2, 2022],
            name={"en": "Test skill", "fr": "Skill de test"},
            description={
                "en": "Test desc",
                "fr": "Desc test"
            }
        )

        payload = {"date": [3, 2022]}
        detail_url = reverse('rest:skill-detail', kwargs={'pk': skill.id})
        res = self.client.patch(detail_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_skill(self):
        """Test updating a skill"""
        skill = Skill.objects.create(
            date=[2, 2022],
            name={"en": "Test skill", "fr": "Skill de test"},
            description={
                "en": "Test desc",
                "fr": "Desc test"
            }
        )

        payload = {"date": [3, 2022]}
        detail_url = reverse('rest:skill-detail', kwargs={'pk': skill.id})
        res = self.admin_client.patch(detail_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        skill.refresh_from_db()
        self.assertEqual(skill.date, payload['date'])

    def test_update_skill_wrong_credentials(self):
        """Test updating a skill with wrong credentials fails correctly"""
        skill = Skill.objects.create(
            date=[2, 2022],
            name={"en": "Test skill", "fr": "Skill de test"},
            description={
                "en": "Test desc",
                "fr": "Desc test"
            }
        )

        payload = {"date": "Wrong credential"}
        detail_url = reverse('rest:skill-detail', kwargs={'pk': skill.id})
        res = self.admin_client.patch(detail_url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        skill.refresh_from_db()
        self.assertNotEqual(skill.date, payload['date'])

    def test_delete_admin_only(self):
        """Test that the deletion requires admin rights"""
        skill = Skill.objects.create(
            date=[2, 2022],
            name={"en": "Test skill", "fr": "Skill de test"},
            description={
                "en": "Test desc",
                "fr": "Desc test"
            }
        )

        detail_url = reverse('rest:skill-detail', kwargs={'pk': skill.id})
        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_skill(self):
        """Test deleting a skill"""
        name = {"en": "Test skill", "fr": "Skill de test"}
        skill = Skill.objects.create(
            date=[2, 2022],
            name=name,
            description={
                "en": "Test desc",
                "fr": "Desc test"
            }
        )

        detail_url = reverse('rest:skill-detail', kwargs={'pk': skill.id})
        res = self.admin_client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        exists = Skill.objects.all().filter(name=name).exists()
        self.assertFalse(exists)
