import pytest

from books.models import Book

pytestmark = pytest.mark.django_db


def test_delete_success(client_authed, book):
    queryset = Book.objects.filter(id=book.id)
    assert queryset.exists()

    response = client_authed.delete(f"/books/{book.id}/")
    data = response.content
    queryset = Book.objects.filter(id=book.id)

    assert response.status_code == 204
    assert not data
    assert not queryset.exists()


def test_delete_not_found(client_authed):
    response = client_authed.delete("/books/843/")
    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "No Book matches the given query."}


def test_delete_not_authenticated(client):
    response = client.delete("/books/25/")
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Authentication credentials were not provided."}


def test_delete_not_authorized(client_authed, other_book):
    response = client_authed.delete(f"/books/{other_book.id}/")
    data = response.json()

    assert response.status_code == 403
    assert data == {"detail": "You do not have permission to perform this action."}
