from django.test import TestCase
from core import models


class SkillModelTest(TestCase):

    def setUp(self):
        self.skill = models.Skill.objects.create(
            name={'en': "MDX", 'fr': "MDX"},
            description={
                "en": "I learned to use MDX",
                "fr": "J'ai appris à utiliser MDX"
            },
            date=[6, 2021]
        )

    def test_name_non_object(self):
        """Test passing anything else than an object fails"""

        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name=[1, 2, 3],
                description={
                    "en": "I learned to use MDX",
                    "fr": "J'ai appris à utiliser MDX"
                },
                date=[6, 2021]
            )

    def test_name_missing_en(self):
        """Test that fails if name.enfield missing"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"fr": "test"},
                description={
                    "en": "I learned to use MDX",
                    "fr": "J'ai appris à utiliser MDX"
                },
                date=[6, 2021]
            )

    def test_name_missing_fr(self):
        """Test that fails if name.fr field missing"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test"},
                description={
                    "en": "I learned to use MDX",
                    "fr": "J'ai appris à utiliser MDX"
                },
                date=[6, 2021]
            )

    def test_name_extra_field(self):
        """Test that fails if extra field other than 'fr' or 'en'"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test", "extra": "wrong"},
                description={
                    "en": "I learned to use MDX",
                    "fr": "J'ai appris à utiliser MDX"
                },
                date=[6, 2021]
            )

    def test_description_non_object(self):
        """Test passing anything else than an object fails"""

        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description=[1, 2, 3],
                date=[6, 2021]
            )

    def test_description_missing_en(self):
        """Test that fails if description.enfield missing"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "fr": "J'ai appris à utiliser MDX"
                },
                date=[6, 2021]
            )

    def test_description_missing_fr(self):
        """Test that fails if description.fr field missing"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": "J'ai appris à utiliser MDX"
                },
                date=[6, 2021]
            )

    def test_description_extra_field(self):
        """Test that fails if extra field other than 'fr' or 'en'"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": "I learned to use MDX",
                    "fr": "J'ai appris à utiliser MDX",
                    "extra": "wrong"
                },
                date=[6, 2021]
            )

    def test_skill_str(self):
        self.assertEqual(str(self.skill), self.skill.name['en'])
