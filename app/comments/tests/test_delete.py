import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from comments.models import Comment

pytestmark = pytest.mark.django_db


def test_delete_success_owner(client_authed, comments):
    id = comments[0].id
    queryset = Comment.objects.filter(id=id)
    assert queryset.exists()

    response = client_authed.delete(f"/comments/{id}/")
    data = response.content
    queryset = Comment.objects.filter(id=id)

    assert response.status_code == 204
    assert not data
    assert not queryset.exists()


def test_delete_success_admin(admin_user, comments):
    id = comments[1].id
    refresh = RefreshToken.for_user(admin_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    queryset = Comment.objects.filter(id=id)
    assert queryset.exists()

    response = client.delete(f"/comments/{id}/")
    data = response.content
    queryset = Comment.objects.filter(id=id)

    assert response.status_code == 204
    assert not data
    assert not queryset.exists()


def test_delete_not_found(client_authed, comments):
    response = client_authed.delete("/comments/1002/")
    data = response.json()

    assert response.status_code == 404
    assert data == {"detail": "No Comment matches the given query."}


def test_delete_not_authenticated(client, comments):
    response = client.delete(f"/comments/{comments[0].id}/")
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Authentication credentials were not provided."}


def test_delete_not_authorized(client_authed, comments):
    response = client_authed.delete(f"/comments/{comments[1].id}/")
    data = response.json()

    assert response.status_code == 403
    assert data == {"detail": "You do not have permission to perform this action."}
