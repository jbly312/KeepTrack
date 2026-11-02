
import pytest
from django.urls import reverse
from rest_framework import status
from users.models import User
# Create your tests here.

@pytest.mark.django_db
def test_register_user(api_client):
    response = api_client.post(
        reverse('register'),
        {'email': 'a@test.com', 'password': 'Str0ngPass123'},
        format='json'
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == 'a@test.com'
    assert "password" not in response.data

    user = User.objects.get(email='a@test.com')
    assert user.check_password('Str0ngPass123')

@pytest.mark.django_db
def test_register_duplicate_email(api_client,make_user):
    make_user('a@test.com')
    response = api_client.post(
        reverse("register"),
        {"email": "a@test.com", "password": "Str0ngPass123"},
        format="json",
    )
    assert User.objects.filter(email="a@test.com").count() == 1
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_weak_password(api_client):

    response = api_client.post(
        reverse("register"),
        {"email": "a@test.com", "password": "123"},
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data

@pytest.mark.django_db
def test_login_success(api_client, make_user):
    make_user('a@test.com', 'Str0ngPass123')
    response = api_client.post(
        reverse("login"),
        {"email": "a@test.com", "password": "Str0ngPass123"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_wrong_password(api_client, make_user):
    make_user('a@test.com', 'Str0ngPass123')
    response = api_client.post(
        reverse("login"),
        {"email": "a@test.com", "password": "WrongPassword"},
        format="json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_me_returns_current_user(api_client, make_user):
    make_user("a@test.com", "Str0ngPass123")
    response = api_client.post(
        reverse("login"),
        {"email": "a@test.com", "password": "Str0ngPass123"},
        format="json",
    )
    token = response.data["access"]

    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    response = api_client.get(
        reverse("me"),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == "a@test.com"

@pytest.mark.django_db
def test_me_unauthorized(api_client, make_user):
    response = api_client.get(
        reverse("me"),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED