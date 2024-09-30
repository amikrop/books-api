from rest_framework import serializers

from books.models import Book
from booksapi.utils import get_user_display


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        return get_user_display(obj.author)

    class Meta:
        model = Book
        fields = "__all__"
