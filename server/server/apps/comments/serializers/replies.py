from server.apps.comments.models import Comment
from server.apps.comments.serializers import CommentSerializer


class ReplyCommentSerializer(CommentSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "reply_to",
            "user",
        )

    def save(self, **kwargs):
        return super().save(**kwargs, user=self.context["request"].user)
