import pytest
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db

User = get_user_model()


def test_register_success(client):
    response = client.post(
        "/auth/register/",
        data={
            "email": "clark.kent@test.org",
            "username": "clark",
            "password": "12345678",
            "first_name": "Clark",
            "last_name": "Kent",
        },
    )
    data = response.json()
    user = User.objects.get(username="clark")

    assert response.status_code == 201
    assert data == {
        "email": "clark.kent@test.org",
        "username": "clark",
        "first_name": "Clark",
        "last_name": "Kent",
    }
    assert user.email == "clark.kent@test.org"
    assert user.username == "clark"
    assert user.first_name == "Clark"
    assert user.last_name == "Kent"
    assert user.check_password("12345678")


def test_register_success_missing_optional_fields(client):
    response = client.post(
        "/auth/register/",
        data={
            "email": "peter.parker@example.com",
            "username": "peter",
            "password": "abcd$efgh123",
        },
    )
    data = response.json()
    user = User.objects.get(username="peter")

    assert response.status_code == 201
    assert data == {"email": "peter.parker@example.com", "username": "peter"}
    assert user.email == "peter.parker@example.com"
    assert user.username == "peter"
    assert user.check_password("abcd$efgh123")


@pytest.mark.parametrize("missing_field", ["email", "username", "password"])
def test_register_missing_required_fields(client, missing_field):
    input_data = {
        "email": "foo@test.com",
        "username": "foo",
        "password": "0987654321abc",
    }
    del input_data[missing_field]

    response = client.post("/auth/register/", data=input_data)
    data = response.json()

    assert response.status_code == 400
    assert data == {missing_field: ["This field is required."]}


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register/",
        data={
            "email": "abcd",
            "username": "abcdef",
            "password": "1234abcd098",
        },
    )
    data = response.json()

    assert response.status_code == 400
    assert data == {"email": ["Enter a valid email address."]}


@pytest.mark.parametrize("field", ["username", "first_name", "last_name"])
def test_register_field_too_long(client, field):
    input_data = {
        "email": "nick@example.org",
        "username": "nick",
        "password": "qwertyuiop",
        "first_name": "Nick",
        "last_name": "Fury",
    }
    input_data[field] = "abc" * 100
    response = client.post("/auth/register/", data=input_data)
    data = response.json()

    assert response.status_code == 400
    assert data == {field: ["Ensure this field has no more than 150 characters."]}


def test_register_invalid_password(client):
    response = client.post(
        "/auth/register/",
        data={
            "email": "abc12@example.com",
            "username": "abc1234",
            "password": "xy56",
        },
    )
    data = response.json()

    assert response.status_code == 400
    assert data == {"password": ["Ensure this field has at least 8 characters."]}


def test_register_existing_email(client):
    response = client.post(
        "/auth/register/",
        data={
            "email": "john@example.com",
            "username": "abcdef",
            "password": "g-34abcd0978",
        },
    )
    data = response.json()

    assert response.status_code == 400
    assert data == {"email": ["Email already exists."]}


def test_register_existing_username(client):
    response = client.post(
        "/auth/register/",
        data={
            "email": "someone@testing.com",
            "username": "john",
            "password": "sdf4abcd0_7k",
        },
    )
    data = response.json()

    assert response.status_code == 400
    assert data == {"username": ["Username already exists."]}
