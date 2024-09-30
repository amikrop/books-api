import pytest
from django.utils.dateparse import parse_datetime

pytestmark = pytest.mark.django_db


def is_valid_datetime(datetime_string):
    try:
        value = parse_datetime(datetime_string)
    except (TypeError, ValueError):
        return False
    return value is not None


def test_list_success(client, other_book, comments):
    response = client.get(f"/books/{other_book.id}/comments/")
    data = response.json()["results"]

    assert response.status_code == 200
    assert len(data) == 2

    for comment in data:
        created_datetime_string = comment.pop("created_datetime")
        assert is_valid_datetime(created_datetime_string)

    assert data == [
        {
            "id": comments[0].id,
            "user": "John Doe <john@example.com>",
            "content": "Hello",
        },
        {"id": comments[1].id, "user": "Bob <bob@test.com>", "content": "Test 123"},
    ]
