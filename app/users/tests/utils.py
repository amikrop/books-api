from rest_framework.test import APIRequestFactory

from books.views import BookViewSet

factory = APIRequestFactory()
view = BookViewSet.as_view({"get": "list"})


def assert_user_anonymous():
    request = factory.get("/books/")
    view(request)
    assert request.user.is_anonymous


def assert_token_authenticates_user(access_token, user):
    request = factory.get("/books/", HTTP_AUTHORIZATION=f"Bearer {access_token}")
    view(request)
    assert request.user == user
