from datetime import date

import pytest

from books.models import Book

pytestmark = pytest.mark.django_db


def test_partial_update_success(client_authed, user, book):
    response = client_authed.patch(
        f"/books/{book.id}/", data={"comments_allowed": True}
    )
    data = response.json()
    book = Book.objects.get(id=book.id)

    assert response.status_code == 200
    assert data == {
        "id": book.id,
        "author": "John Doe <john@example.com>",
        "title": "Magic Land",
        "genre": "Fantasy",
        "publication_date": "2024-09-27",
        "comments_allowed": True,
    }
    assert book.id == book.id
    assert book.author == user
    assert book.title == "Magic Land"
    assert book.genre == "Fantasy"
    assert book.publication_date == date(2024, 9, 27)
    assert book.comments_allowed is True


def test_partial_update_not_found(client_authed):
    response = client_authed.patch(
        "/books/602/", data={"title": "Foo", "publication_date": "2013-10-10"}
    )
    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "No Book matches the given query."}


def test_partial_update_not_authenticated(client):
    response = client.patch(
        "/books/32/",
        data={"title": "My Magical Land", "publication_date": "2020-02-10"},
    )
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Authentication credentials were not provided."}


def test_partial_update_not_authorized(client_authed, other_book):
    response = client_authed.patch(
        f"/books/{other_book.id}/",
        data={
            "title": "Baz",
            "publication_date": "2023-05-15",
            "genre": "Memoirs",
        },
    )
    data = response.json()

    assert response.status_code == 403
    assert data == {"detail": "You do not have permission to perform this action."}
