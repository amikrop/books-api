from datetime import date

import pytest

from books.models import Book

pytestmark = pytest.mark.django_db


def test_update_success(client_authed, user, book):
    response = client_authed.put(
        f"/books/{book.id}/",
        data={
            "title": "The Magical Land",
            "publication_date": "2022-02-08",
            "comments_allowed": True,
        },
    )
    data = response.json()
    book = Book.objects.get(id=book.id)

    assert response.status_code == 200
    assert data == {
        "id": book.id,
        "author": "John Doe <john@example.com>",
        "title": "The Magical Land",
        "genre": "Fantasy",
        "publication_date": "2022-02-08",
        "comments_allowed": True,
    }
    assert book.id == book.id
    assert book.author == user
    assert book.title == "The Magical Land"
    assert book.genre == "Fantasy"
    assert book.publication_date == date(2022, 2, 8)
    assert book.comments_allowed is True


def test_update_not_found(client_authed):
    response = client_authed.put(
        "/books/450/", data={"title": "Nonexistent", "publication_date": "2010-12-10"}
    )
    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "No Book matches the given query."}


def test_update_not_authenticated(client):
    response = client.put(
        "/books/87/",
        data={"title": "Some Magical Land", "publication_date": "2022-02-09"},
    )
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Authentication credentials were not provided."}


def test_update_not_authorized(client_authed, other_book):
    response = client_authed.put(
        f"/books/{other_book.id}/",
        data={
            "title": "My Memoirs",
            "publication_date": "2023-05-10",
            "genre": "Memoirs",
        },
    )
    data = response.json()

    assert response.status_code == 403
    assert data == {"detail": "You do not have permission to perform this action."}


def test_update_missing_required_fields(client_authed):
    response = client_authed.post("/books/", data={"publication_date": "2025-01-01"})
    data = response.json()

    assert response.status_code == 400
    assert data == {"title": ["This field is required."]}
