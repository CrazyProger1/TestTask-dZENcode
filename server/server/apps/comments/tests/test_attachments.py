import io

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from server.apps.comments.models import Comment, CommentAttachment


class TestCommentAttachmentViewSet(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpass123",
            is_active=True,
        )
        self.comment = Comment.objects.create(text="Test comment", user=self.user)
        self.attachment = CommentAttachment.objects.create(
            comment=self.comment, file="test_file.txt", type="TXT"
        )
        self.client.force_authenticate(user=self.user)
        self.photo_filename = "test.png"

    def generate_photo_file(self):
        file = io.BytesIO(b"test")
        file.name = self.photo_filename
        file.seek(0)
        return file

    def test_create_attachment(self):
        data = {"file": self.generate_photo_file()}
        response = self.client.post(
            f"/api/v1/comments/{self.comment.pk}/attachments/", data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_attachments(self):
        response = self.client.get(f"/api/v1/comments/{self.comment.pk}/attachments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_attachment(self):
        response = self.client.get(f"/api/v1/comments/{self.comment.pk}/attachments/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["type"], "TXT")

    def test_update_attachment(self):
        data = {"file": self.generate_photo_file()}
        response = self.client.patch(
            f"/api/v1/comments/{self.comment.pk}/attachments/1/",
            data,
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attachment.refresh_from_db()
        self.assertEqual(self.attachment.type, "IMG")

    def test_delete_attachment(self):
        response = self.client.delete(
            f"/api/v1/comments/{self.comment.pk}/attachments/1/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            CommentAttachment.objects.filter(pk=self.attachment.pk).exists()
        )
