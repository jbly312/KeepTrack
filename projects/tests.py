from django.test import TestCase, Client
import pytest

from django.urls import reverse
from rest_framework import status
from users.models import User
from projects.models import Project, ProjectMember


# Create your tests here.


@pytest.mark.django_db
def test_project_create(api_client, make_user, auth_client):
    user = make_user("a@test.com")
    client = auth_client(user)
    response = client.post(
        reverse("projects"),
        {"name": "test", "slug": "test"},
        format="json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert ProjectMember.objects.filter(role=ProjectMember.Role.OWNER, project_id=response.data["id"],
                                        user=user).exists()


@pytest.mark.django_db
def test_project_list_shows_only_own(make_user, auth_client, make_project):
    user_a = make_user("a@test.com")
    user_b = make_user("b@test.com")
    client_b = auth_client(user_b)
    project_a = make_project(user_a, "test_1", "test_1")
    project_b = make_project(user_b, "test_2", "test_2")

    response = client_b.get(
        reverse("projects"),
    )
    ids = [project["id"] for project in response.data]
    assert response.status_code == status.HTTP_200_OK
    assert project_a.id not in ids
    assert project_b.id in ids


@pytest.mark.django_db
def test_foreign_project_returns_404(make_user, auth_client, make_project):
    user_a = make_user("a@test.com")
    user_stranger = make_user("stranger@test.com")
    project_a = make_project(user_a, "test_1", "test_1")
    client_stranger = auth_client(user_stranger)

    response = client_stranger.get(
        reverse("projects_detail", kwargs={"pk": project_a.id}),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize("role, expected_status, expected_name", [
    (ProjectMember.Role.VIEWER, status.HTTP_403_FORBIDDEN, "test_1"),
    (ProjectMember.Role.EDITOR, status.HTTP_200_OK, "new name"),
    (ProjectMember.Role.OWNER, status.HTTP_200_OK,"new name"),
])
def test_project_update_by_role(
        role,
        expected_status,
        make_user,
        auth_client,
        make_project,
        add_member,
        expected_name
):
    owner = make_user("owner@test.com")
    project = make_project(owner, "test_1", "test_1")
    member = make_user("member@test.com")
    add_member(project, member, role)
    client = auth_client(member)

    response = client.patch(
        reverse("projects_detail", kwargs={"pk": project.id}),
        {"name": "new name"},
        format="json",
    )

    project.refresh_from_db()
    assert response.status_code == expected_status
    assert project.name == expected_name


@pytest.mark.django_db
@pytest.mark.parametrize("role, expected_status, should_exist", [
    (ProjectMember.Role.VIEWER, status.HTTP_403_FORBIDDEN, True),
    (ProjectMember.Role.EDITOR, status.HTTP_403_FORBIDDEN, True),
    (ProjectMember.Role.OWNER, status.HTTP_204_NO_CONTENT, False),
])
def test_project_delete_by_role(
        role,
        expected_status,
        make_user,
        auth_client,
        make_project,
        add_member,
        should_exist
):
    owner = make_user("owner@test.com")
    project = make_project(owner, "test_1", "test_1")
    member = make_user("member@test.com")
    add_member(project, member, role)
    client = auth_client(member)

    response = client.delete(
        reverse("projects_detail", kwargs={"pk": project.id})
    )

    assert Project.objects.filter(id=project.id).exists() == should_exist
    assert response.status_code == expected_status