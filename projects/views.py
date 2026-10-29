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
