import pytest
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from comments.models import Comment

pytestmark = pytest.mark.django_db


def datetimes_almost_equal(first, second):
    return first.replace(second=0, microsecond=0) == second.replace(
        second=0, microsecond=0
    )


def test_create_success(client_authed, user, other_book):
    response = client_authed.post(
        f"/books/{other_book.id}/comments/", data={"content": "Nice book, worth it."}
    )
    data = response.json()
    id = data.pop("id")
    created_datetime_string = data.pop("created_datetime")
    created_datetime = parse_datetime(created_datetime_string)
    comment = Comment.objects.get(id=id)
    now = timezone.now()

    assert response.status_code == 201
    assert data == {
        "user": "John Doe <john@example.com>",
        "content": "Nice book, worth it.",
    }
    assert datetimes_almost_equal(created_datetime, now)
    assert comment.id == id
    assert comment.content == "Nice book, worth it."
    assert datetimes_almost_equal(comment.created_datetime, now)
    assert comment.book == other_book
    assert comment.user == user


def test_create_not_authenticated(client, other_book):
    response = client.post(
        f"/books/{other_book.id}/comments/", data={"content": "Testing"}
    )
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Authentication credentials were not provided."}


def test_create_missing_required_fields(client_authed, other_book):
    response = client_authed.post(f"/books/{other_book.id}/comments/")
    data = response.json()

    assert response.status_code == 400
    assert data == {"content": ["This field is required."]}


def test_create_not_found_book(client_authed):
    response = client_authed.post("/books/332/comments/", data={"content": "abc"})
    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "No Book matches the given query."}


def test_create_not_allowed(client_authed, book):
    response = client_authed.post(f"/books/{book.id}/comments/")
    data = response.json()

    assert response.status_code == 403
    assert data == {"detail": "You do not have permission to perform this action."}
