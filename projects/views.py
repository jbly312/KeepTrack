from django.shortcuts import render
from rest_framework import generics, permissions, serializers
from django.db import transaction
from projects.models import Project, ProjectMember
from projects.serializers import ProjectSerializer, MemberSerializer
from projects.permissions import ProjectRolePermission, ProjectMemberPermission
from django.shortcuts import get_object_or_404
# Create your views here.

class ProjectListView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(project=project, user = self.request.user, role = ProjectMember.Role.OWNER)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectRolePermission]
    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user)


class ProjectMemberListView(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectMemberPermission]
    def get_project(self):
        return get_object_or_404(Project, pk = self.kwargs['project_id'])

    def get_queryset(self):
        return ProjectMember.objects.filter(project=self.get_project())

    def perform_create(self, serializer):
        project = self.get_project()
        user = serializer.validated_data['user']
        if ProjectMember.objects.filter(project=project, user=user).exists():
            raise serializers.ValidationError({"user_email": "User is already a member of this project"})
        serializer.save(project=project)

class ProjectMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectMemberPermission]
    http_method_names = ['get', 'patch', 'delete']

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_object(self):
        return get_object_or_404(ProjectMember, project = self.get_project(), user_id = self.kwargs['user_id'])

    def check_last_owner(self, member):
        if member.role != ProjectMember.Role.OWNER:
            return
        other_owners = ProjectMember.objects.filter(
            project= member.project,
            role = ProjectMember.Role.OWNER).exclude(pk=member.pk)
        if not other_owners.exists():
            raise serializers.ValidationError("A project must keep at least one owner")

    def perform_destroy(self, instance):
        self.check_last_owner(instance)
        instance.delete()

    def perform_update(self, serializer):
        new_role = serializer.validated_data.get("role")
        if new_role and new_role != ProjectMember.Role.OWNER:
            self.check_last_owner(serializer.instance)
        serializer.save()