from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from server.apps.comments.models import Comment


class TestCommentViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpass123",
            is_active=True,
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="testuser2@test.com",
            password="testpass1234",
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_comment(self):
        text = "test comment"

        response = self.client.post("/api/v1/comments/", data={"text": text})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Comment.objects.get(pk=response.data["id"]).text, text)

    def test_list_comments(self):
        Comment.objects.create(user=self.user, text="comment 1")
        Comment.objects.create(user=self.user, text="comment 2")

        response = self.client.get("/api/v1/comments/")
        comments = response.data["results"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(comments), 2)

    def test_retrieve_comment(self):
        comment = Comment.objects.create(user=self.user, text="test comment")

        response = self.client.get(f"/api/v1/comments/{comment.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "test comment")

    def test_update_comment(self):
        updated_text = "updated comment"

        comment = Comment.objects.create(user=self.user, text="test comment")

        response = self.client.put(
            f"/api/v1/comments/{comment.id}/", {"text": updated_text}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(pk=comment.id).text, updated_text)

    def test_delete_comment(self):
        comment = Comment.objects.create(user=self.user, text="test comment")

        response = self.client.delete(f"/api/v1/comments/{comment.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=comment.id)
