from rest_framework import permissions
from projects.models import ProjectMember

class ProjectRolePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        member = ProjectMember.objects.filter(project=obj, user=request.user).first()
        if member is None:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE':
            return ProjectMember.Role.OWNER == member.role

        return member.role in (ProjectMember.Role.OWNER, ProjectMember.Role.EDITOR)

class ProjectMemberPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        project = view.get_project()
        member = ProjectMember.objects.filter(project=project, user=request.user).first()

        if member is None:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        return member.role == ProjectMember.Role.OWNER

class ProjectEditorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        project = view.get_project()
        member = ProjectMember.objects.filter(project=project, user=request.user).first()

        if member is None:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        return member.role in (ProjectMember.Role.OWNER, ProjectMember.Role.EDITOR)
