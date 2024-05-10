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
            "has_attachment",
        )

    def save(self, **kwargs):
        user = kwargs.pop("user", None)
        if not user:
            user = self.context["request"].user
        return super().save(**kwargs, user=user)
