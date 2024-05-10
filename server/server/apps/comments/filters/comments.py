import django_filters as filters

from server.apps.comments.models import Comment


class CommentFilter(filters.FilterSet):
    user__username = filters.CharFilter(lookup_expr='icontains')
    user__email = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Comment
        fields = (
            "user",
            "created_at",
        )
