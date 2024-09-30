from datetime import date

import pytest

from books.models import Book

pytestmark = pytest.mark.django_db


def test_create_success(client_authed, user):
    response = client_authed.post(
        "/books/", data={"title": "My Book", "publication_date": "2022-02-07"}
    )
    data = response.json()
    id = data.pop("id")
    book = Book.objects.get(id=id)

    assert response.status_code == 201
    assert isinstance(id, int)
    assert data == {
        "author": "John Doe <john@example.com>",
        "title": "My Book",
        "genre": "",
        "publication_date": "2022-02-07",
        "comments_allowed": False,
    }
    assert book.author == user
    assert book.title == "My Book"
    assert book.genre == ""
    assert book.publication_date == date(2022, 2, 7)
    assert book.comments_allowed is False


def test_create_not_authenticated(client):
    response = client.post(
        "/books/", data={"title": "Testing", "publication_date": "2021-03-11"}
    )
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.parametrize("missing_field", ["title", "publication_date"])
def test_create_missing_required_fields(client_authed, missing_field):
    input_data = {"title": "The Title", "publication_date": "2018-06-02"}
    del input_data[missing_field]

    response = client_authed.post("/books/", data=input_data)
    data = response.json()

    assert response.status_code == 400
    assert data == {missing_field: ["This field is required."]}
