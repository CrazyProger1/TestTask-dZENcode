import django_filters as filters

from .models import Comment


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = ("user", "created_at",)
