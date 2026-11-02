from users.models import User
from projects.models import Project, ProjectMember
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def make_user(db):
    def _make(email, password="Str0ngPass123"):
        return User.objects.create_user(email, password=password)

    return _make


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client():
    def _make(user):
        client = APIClient()
        client.force_authenticate(user)
        return client

    return _make


@pytest.fixture
def make_project(db):
    def _make(owner, name="test", slug="test"):
        project = Project.objects.create(owner=owner, name=name, slug=slug)
        ProjectMember.objects.create(project=project, user=owner, role=ProjectMember.Role.OWNER)
        return project

    return _make

@pytest.fixture
def add_member(db):
    def _make(project, user, role):
        member = ProjectMember.objects.create(project=project, user=user, role=role)
        return member
    return _make