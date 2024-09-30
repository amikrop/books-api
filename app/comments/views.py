from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from books.models import Book
from comments.models import Comment
from comments.permissions import CommentPermission
from comments.serializers import CommentSerializer


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def initial(self, *args, **kwargs):
        if "book_pk" in kwargs:
            # In create or list view, store parent book
            self.book = get_object_or_404(Book, pk=kwargs["book_pk"])

        super().initial(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(book=self.book, user=self.request.user)

    def get_queryset(self):
        if "book_pk" in self.kwargs:
            # In create or list view, refer to parent book
            return Comment.objects.filter(book=self.book)

        return Comment.objects.all()
