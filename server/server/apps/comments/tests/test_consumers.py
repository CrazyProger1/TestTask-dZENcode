from django.contrib.auth.models import User
from django.test import TestCase
from channels.testing import WebsocketCommunicator

from server.apps.comments.consumers import CommentConsumer


class TestCommentConsumer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@test.com",
            password="testpass123",
            is_active=True,
        )
