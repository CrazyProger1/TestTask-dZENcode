from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from server.apps.comments.models import Comment, CommentLike


class TestCommentLikeViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpass123",
            is_active=True,
        )
        self.comment = Comment.objects.create(text="Test comment", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_like(self):
        data = {"positive": True}
        response = self.client.post(f"/api/v1/comments/{self.comment.pk}/likes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            CommentLike.objects.filter(user=self.user, comment=self.comment).exists()
        )

    def test_recreate_existing_like(self):
        like = CommentLike.objects.create(
            user=self.user, comment=self.comment, positive=True
        )
        data = {"positive": False}
        response = self.client.post(f"/api/v1/comments/{self.comment.pk}/likes/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        like.refresh_from_db()
        self.assertFalse(like.positive)

    def test_list_likes(self):
        CommentLike.objects.create(user=self.user, comment=self.comment, positive=True)
        response = self.client.get(f"/api/v1/comments/{self.comment.pk}/likes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_like(self):
        like = CommentLike.objects.create(
            user=self.user, comment=self.comment, positive=True
        )
        data = {"positive": False}
        response = self.client.patch(f"/api/v1/comments/{self.comment.pk}/likes/{like.pk}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        like.refresh_from_db()
        self.assertFalse(like.positive)

    def test_delete_like(self):
        like = CommentLike.objects.create(user=self.user, comment=self.comment, positive=True)
        response = self.client.delete(f"/api/v1/comments/{self.comment.pk}/likes/{like.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            CommentLike.objects.filter(user=self.user, comment=self.comment).exists()
        )
