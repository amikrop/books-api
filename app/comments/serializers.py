from rest_framework import serializers

from booksapi.utils import get_user_display
from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return get_user_display(obj.user)

    class Meta:
        model = Comment
        exclude = ["book"]
