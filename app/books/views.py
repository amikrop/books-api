from rest_framework import viewsets

from books.models import Book
from books.permissions import IsOwnerOrReadOnly
from books.search import filter_books
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all()

        if "pk" in self.kwargs:
            # In detail view, do not filter
            return queryset

        return filter_books(self.request, queryset)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
