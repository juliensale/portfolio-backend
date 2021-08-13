from django.test import TestCase
from core import models
from unittest.mock import patch


class SkillModelTest(TestCase):

    def setUp(self):
        self.skill = models.Skill.objects.create(
            name={'en': "MDX", 'fr': "MDX"},
            description={
                "en": ["I learned to use MDX"],
                "fr": ["J'ai appris à utiliser MDX"]
            },
            date=[6, 2021]
        )

    def test_name_non_object(self):
        """Test passing anything else than an object fails"""

        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name=[1, 2, 3],
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"]
                },
                date=[6, 2021]
            )

    def test_name_missing_en(self):
        """Test that fails if name.enfield missing"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"]
                },
                date=[6, 2021]
            )

    def test_name_missing_fr(self):
        """Test that fails if name.fr field missing"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"]
                },
                date=[6, 2021]
            )

    def test_name_strings(self):
        """Test that name.en & name.fr must be strings"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": 3, "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"]
                },
                date=[6, 2021]
            )
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": [1, 2]},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"]
                },
                date=[6, 2021]
            )

    def test_name_extra_field(self):
        """Test that fails if extra field other than 'fr' or 'en'"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test", "extra": "wrong"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"]
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
                    "fr": ["J'ai appris à utiliser MDX"]
                },
                date=[6, 2021]
            )

    def test_description_missing_fr(self):
        """Test that fails if description.fr field missing"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["J'ai appris à utiliser MDX"]
                },
                date=[6, 2021]
            )

    def test_description_string_arrays(self):
        """Test that description.en & description.fr must be string arrays"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": "Test",
                    "fr": ["J'ai appris à utiliser MDX"]
                },
                date=[6, 2021]
            )
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": [1, 2, 3]
                },
                date=[6, 2021]
            )

    def test_description_extra_field(self):
        """Test that fails if extra field other than 'fr' or 'en'"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                    "extra": ["wrong"]
                },
                date=[6, 2021]
            )

    def test_date_array(self):
        """Test that fails if date not array"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                },
                date={"a": "test"}
            )

    def test_date_array_length(self):
        """Test that fails if date not of length 2"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                },
                date=[1, 2, 3]
            )

    def test_date_month(self):
        """Test that fails with month outside of [1,12]"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                },
                date=[0, 2021]
            )
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                },
                date=[13, 2021]
            )

    def test_date_year(self):
        """Test that fails with year outside of [2000,2100]"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                },
                date=[1, 1999]
            )
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                },
                date=[1, 2101]
            )

    def test_date_ints(self):
        """Test that date values must be int"""
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                },
                date=["a", 2021]
            )
        with self.assertRaises(ValueError):
            models.Skill.objects.create(
                name={"en": "test", "fr": "test"},
                description={
                    "en": ["I learned to use MDX"],
                    "fr": ["J'ai appris à utiliser MDX"],
                },
                date=[6, [1, 2, 3]]
            )

    def test_skill_str(self):
        self.assertEqual(str(self.skill), self.skill.name['en'])

    def test_skill_valid(self):
        """Test creating a valid skill"""
        models.Skill.objects.create(
            name={"en": "test", "fr": "test"},
            description={
                "en": ["I learned to use MDX"],
                "fr": ["J'ai appris à utiliser MDX"]
            },
            date=[6, 2021]
        )


class TechnologyModelTests(TestCase):

    def setUp(self):
        self.technology = models.Technology.objects.create(
            name="Test"
        )

    @patch('uuid.uuid4')
    def test_image_file_name_uuid(self, mock_uuid):
        """Test that imge is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.technology_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/technology/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    def test_technology_str(self):
        self.assertEqual(str(self.technology), self.technology.name)


class ReviewModelTests(TestCase):

    def setUp(self):
        self.review = models.Review.objects.create(
            author="Test author",
            message={"en": "Test message", "fr": "Message de test"}
        )

    def test_update_code_generation(self):
        """Test that update_code is generated when
        and only when the object is created"""
        code = self.review.update_code
        self.review.author = "Test author 2"
        self.review.save()
        self.review.refresh_from_db()
        self.assertEqual(code, self.review.update_code)

    def test_modified(self):
        """Test that the modified field doesn't change on creation"""
        self.assertFalse(self.review.modified)
        self.review.author = "Test author 2"
        self.review.save()
        self.review.refresh_from_db()
        self.assertTrue(self.review.modified)

    def test_message_missing_language(self):
        """Test that fails if message.en or message.fr is missing"""
        with self.assertRaises(ValueError):
            models.Review.objects.create(
                author="Test author",
                message={"en": "Test message"}
            )
        with self.assertRaises(ValueError):
            models.Review.objects.create(
                author="Test author",
                message={"fr": "Message de test"}
            )

    def test_message_non_object(self):
        """Test giving anything else than an object for the message fails"""
        with self.assertRaises(ValueError):
            models.Review.objects.create(
                author="Test author",
                message="Test"
            )

    def test_message_extra_key(self):
        """Test giving an extra key to message fails"""
        with self.assertRaises(ValueError):
            models.Review.objects.create(
                author="Test author",
                message={"en": "Test message",
                         "fr": "Message de test", "extra": "Extra field"}
            )

    def test_message_str(self):
        """Test that the language keys must be strings"""
        with self.assertRaises(ValueError):
            models.Review.objects.create(
                author="Test author",
                message={"en": [1, 2, 3], "fr": "Message de test"}
            )
        with self.assertRaises(ValueError):
            models.Review.objects.create(
                author="Test author",
                message={"en": "Test message", "fr": [1, 2, 3]}
            )

        models.Review.objects.create(
            author="Test author",
            message={"en": "Test message", "fr": "Message de test"}
        )

    def test_review_str(self):
        self.assertEqual(str(self.review), self.review.message['en'])


class ProjectModelTests(TestCase):

    def setUp(self):
        self.project = models.Project.objects.create(
            name={"en": "en", "fr": "fr"},
            description={"en": ["en description"], "fr": ["fr description"]}
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), self.project.name['en'])

    def test_project_creates_review(self):
        """Tests that creating a project automatically
        creates an associated review"""

        exists = models.Review.objects.filter(project=self.project).exists()
        self.assertTrue(exists)

    def test_name_missing_language(self):
        """Test that fails if name.en or name.fr is missing"""
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "azer"},
                description={"en": ["en description"],
                             "fr": ["fr description"]}
            )
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"fr": "azer"},
                description={"en": ["en description"],
                             "fr": ["fr description"]}
            )

    def test_name_non_object(self):
        """Test giving anything else than an object for the name fails"""
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name=[1, 2, 3],
                description={"en": ["en description"],
                             "fr": ["fr description"]}
            )

    def test_name_extra_key(self):
        """Test giving an extra key to name fails"""
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "aze", "fr": "azer", "extra": "azer"},
                description={"en": ["en description"],
                             "fr": ["fr description"]}
            )

    def test_name_str(self):
        """Test that the language keys must be strings"""
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": [1, 2, 3], "fr": "azer"},
                description={"en": ["en description"],
                             "fr": ["fr description"]}
            )
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "aze", "fr": [1, 2, 3]},
                description={"en": ["en description"],
                             "fr": ["fr description"]}
            )

    def test_description_missing_language(self):
        """Test that fails if description.en or description.fr is missing"""
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "azer", "fr": "azer"},
                description={"en": ["Test desc"]}
            )
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "azer", "fr": "azer"},
                description={"fr": ["Test desc"]}
            )

    def test_description_non_object(self):
        """Test giving anything else than an object
        for the description fails"""
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "azer", "fr": "azer"},
                description=[1, 2, 3]
            )

    def test_description_extra_key(self):
        """Test giving an extra key to description fails"""
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "azer", "fr": "azer"},
                description={"en": ["azer"], "fr": ["aezr"], "extra": ["azer"]}
            )

    def test_description_str_array(self):
        """Test that the language keys must be string arrays"""
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "azer", "fr": "azer"},
                description={"en": ["azer"], "fr": [1, 2, 3]}
            )
        with self.assertRaises(ValueError):
            models.Project.objects.create(
                name={"en": "azer", "fr": "azer"},
                description={"en": "Test", "fr": ["azer"]}
            )

    def test_create_valid(self):
        """Test creating a valid project object"""
        models.Project.objects.create(
            name={"en": "Test en", "fr": "Test fr"},
            description={"en": ["Test desc"], "fr": ["Desc test"]}
        )
