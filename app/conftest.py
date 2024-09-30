import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from books.models import Book
from comments.models import Comment

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        "john", "john@example.com", first_name="John", last_name="Doe"
    )


@pytest.fixture
def other_user():
    return User.objects.create_user("bob", "bob@test.com", first_name="Bob")


@pytest.fixture(autouse=True)
def book(user):
    return Book.objects.create(
        title="Magic Land",
        genre="Fantasy",
        publication_date="2024-09-27",
        author=user,
    )


@pytest.fixture(autouse=True)
def other_book(other_user):
    return Book.objects.create(
        title="Some Memoirs",
        publication_date="2023-05-10",
        comments_allowed=True,
        author=other_user,
    )


@pytest.fixture
def comments(user, other_user, other_book):
    return Comment.objects.bulk_create(
        [
            Comment(content="Hello", book=other_book, user=user),
            Comment(content="Test 123", book=other_book, user=other_user),
        ]
    )


@pytest.fixture
def client_authed(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
