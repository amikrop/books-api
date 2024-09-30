import pytest

from users.tests.utils import assert_token_authenticates_user, assert_user_anonymous

pytestmark = pytest.mark.django_db


def test_login_success(client, user):
    user.set_password("secret.*321")
    user.save()
    assert_user_anonymous()

    response = client.post(
        "/auth/login/", data={"username": "john", "password": "secret.*321"}
    )
    data = response.json()

    assert response.status_code == 200
    assert set(data) == {"access", "refresh"}
    assert_token_authenticates_user(data["access"], user)


@pytest.mark.parametrize("missing_field", ["username", "password"])
def test_login_missing_required_fields(client, missing_field):
    input_data = {"username": "some_username", "password": "some_password"}
    del input_data[missing_field]

    response = client.post("/auth/login/", data=input_data)
    data = response.json()

    assert response.status_code == 400
    assert data == {missing_field: ["This field is required."]}


def test_login_wrong_credentials(client):
    response = client.post(
        "/auth/login/", data={"username": "someone", "password": "wrong123"}
    )
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "No active account found with the given credentials"}
