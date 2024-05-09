import django_filters as filters

from server.apps.comments.models import Comment


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = (
            "user",
            "created_at",
        )
