from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from server.apps.comments.models import Comment


class TestReplyViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpass123",
            is_active=True,
        )
        self.client.force_authenticate(user=self.user)
        self.comment = Comment.objects.create(user=self.user, text="Test comment")

    def test_create_reply(self):
        data = {"text": "Reply to the comment"}
        response = self.client.post(
            f"/api/v1/comments/{self.comment.id}/replies/", data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "Reply to the comment")

    def test_list_replies(self):
        reply = Comment.objects.create(
            user=self.user, text="Reply to the comment", reply_to=self.comment
        )
        response = self.client.get(f"/api/v1/comments/{self.comment.id}/replies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["text"], "Reply to the comment")

    def test_retrieve_reply(self):
        reply = Comment.objects.create(
            user=self.user, text="Reply to the comment", reply_to=self.comment
        )
        response = self.client.get(
            f"/api/v1/comments/{self.comment.id}/replies/{reply.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Reply to the comment")

    def test_update_reply(self):
        reply = Comment.objects.create(
            user=self.user, text="Reply to the comment", reply_to=self.comment
        )
        updated_data = {"text": "Updated reply"}
        response = self.client.put(
            f"/api/v1/comments/{self.comment.id}/replies/{reply.id}/",
            data=updated_data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Updated reply")

    def test_delete_reply(self):
        reply = Comment.objects.create(
            user=self.user, text="Reply to the comment", reply_to=self.comment
        )
        response = self.client.delete(
            f"/api/v1/comments/{self.comment.id}/replies/{reply.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(pk=reply.id)
