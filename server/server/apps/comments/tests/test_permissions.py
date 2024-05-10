from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from server.apps.comments.models import Comment
from server.apps.comments.permissions import IsCommentOwnerOrReadOnly, CanAddAttachments


class TestPermissions(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.comment_owner = User.objects.create_user(
            username="comment_owner",
            email="comment_owner@test.com",
            password="commentpass123",
            is_active=True,
        )
        self.other_user = User.objects.create_user(
            username="other_user",
            email="other_user@test.com",
            password="otherpass123",
            is_active=True,
        )
        self.comment = Comment.objects.create(
            user=self.comment_owner, text="test comment"
        )

    def test_is_comment_owner_or_read_only_permission(self):
        request = self.factory.put("api/v1/comments/")

        request.user = self.comment_owner
        self.assertTrue(
            IsCommentOwnerOrReadOnly().has_object_permission(
                request, None, self.comment
            )
        )

        request.user = self.other_user
        self.assertFalse(
            IsCommentOwnerOrReadOnly().has_object_permission(
                request, None, self.comment
            )
        )

    def test_can_add_attachments_permission(self):
        request = self.factory.post("api/v1/comments/")

        view = type("view", (), {"kwargs": {"comment_id": self.comment.id}})

        request.user = self.comment_owner
        self.assertTrue(CanAddAttachments().has_permission(request, view))

        request.user = self.other_user
        self.assertFalse(CanAddAttachments().has_permission(request, view))
