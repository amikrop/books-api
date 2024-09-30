import pytest

pytestmark = pytest.mark.django_db


def test_list_success(client, book, other_book):
    response = client.get("/books/")
    data = response.json()["results"]

    assert response.status_code == 200
    assert len(data) == 2
    assert data == [
        {
            "id": book.id,
            "author": "John Doe <john@example.com>",
            "title": "Magic Land",
            "genre": "Fantasy",
            "publication_date": "2024-09-27",
            "comments_allowed": False,
        },
        {
            "id": other_book.id,
            "author": "Bob <bob@test.com>",
            "title": "Some Memoirs",
            "genre": "",
            "publication_date": "2023-05-10",
            "comments_allowed": True,
        },
    ]
