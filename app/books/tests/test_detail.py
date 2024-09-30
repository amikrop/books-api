import pytest

pytestmark = pytest.mark.django_db


def test_detail_success(client, book):
    response = client.get(f"/books/{book.id}/")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "id": book.id,
        "author": "John Doe <john@example.com>",
        "title": "Magic Land",
        "genre": "Fantasy",
        "publication_date": "2024-09-27",
        "comments_allowed": False,
    }


def test_detail_not_found(client):
    response = client.get("/books/952/")
    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "No Book matches the given query."}
