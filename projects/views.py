from django.shortcuts import render
from rest_framework import generics
from django.db import transaction
from projects.models import Project, ProjectMember
from projects.serializers import ProjectSerializer
# Create your views here.

class ProjectListView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(members__user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(project=project, user = self.request.user, role = ProjectMember.Role.OWNER)