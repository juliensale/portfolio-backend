import os
from django.test import TestCase
from core.models import Review
from rest.serializers import ReviewSerializer
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

REVIEW_URL = reverse('rest:review-list')


class ReviewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_client = APIClient()
        self.admin_client.credentials(
            HTTP_AUTHORIZATION='Token ' + os.environ['ADMIN_TOKEN'])

    def test_retrieve_reviews(self):
        """Tests retrieving reviews"""
        Review.objects.create(author="", message="")
        Review.objects.create(author="Google CEO",
                              message="Good, very gud!", modified=True)
        Review.objects.create(author="Google CEO",
                              message="Good, very gud!", modified=True)

        res = self.client.get(REVIEW_URL)
        reviews = Review.objects.all().filter(modified=True).order_by('author')
        serializer = ReviewSerializer(reviews, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['author'], serializer.data[0]['author'])

    def test_create_admin_only(self):
        """Tests that the creation requires admin rights"""
        res = self.client.post(REVIEW_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_review(self):
        """Tests creating a review"""
        res = self.admin_client.post(REVIEW_URL)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Review.objects.all().filter(id=res.data['id']).exists()
        self.assertTrue(exists)

    def test_update_code_only(self):
        """Tests that the update requires the update_code"""
        review = Review.objects.create(
            author="", message="")
        payload = {"author": "Google CEO", "message": "Good, very gud!"}
        update_url = reverse('rest:review-update-with-code')
        res = self.client.patch(update_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        review.refresh_from_db()
        self.assertNotEqual(review.author, payload['author'])

    def test_update_wrong_code(self):
        """Tests that updating with a wrong code fails correctly"""
        review = Review.objects.create(
            author="", message="")
        payload = {"author": "Google CEO",
                   "message": "Good, very gud!", "update_code": "30a"}
        update_url = reverse('rest:review-update-with-code')
        res = self.client.patch(update_url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        review.refresh_from_db()
        self.assertNotEqual(review.author, payload['author'])

    def test_update_review(self):
        """Tests updating a review with its update code"""
        review = Review.objects.create(
            author="", message="")
        payload = {"author": "Google CEO", "message": "Good, very gud!",
                   "update_code": review.update_code}
        update_url = reverse('rest:review-update-with-code')
        res = self.client.patch(update_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertEqual(review.author, payload['author'])
        self.assertEqual(review.update_code, payload['update_code'])

    def test_update_review_wrong_credentials(self):
        """Tests updating a review with correct code but wrong credentials
        fails correctly"""
        review = Review.objects.create(
            author="", message="")
        payload = {"author": [1, 2, 3], "message": "Good, very gud!",
                   "update_code": review.update_code}
        update_url = reverse('rest:review-update-with-code')
        res = self.client.patch(update_url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        review.refresh_from_db()
        self.assertNotEqual(review.author, payload['author'])

    def test_delete_admin_only(self):
        """Tests that the deletion requires admin rights"""
        review = Review.objects.create(
            author="Google CEO", message="Good, very gud!")
        detail_url = reverse('rest:review-detail', kwargs={'pk': review.id})
        res = self.client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review(self):
        """Test deleting a review"""
        review = Review.objects.create(
            author="Google CEO", message="Good, very gud!")
        detail_url = reverse('rest:review-detail', kwargs={'pk': review.id})
        res = self.admin_client.delete(detail_url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
