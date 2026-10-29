from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, permissions
from cases.serializers import SuiteSerializer
from projects.permissions import ProjectEditorPermission
from projects.models import Project
from cases.models import Suite
# Create your views here.

class SuiteListView(generics.ListCreateAPIView):
    serializer_class = SuiteSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectEditorPermission]

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs['project_id'])

    def get_queryset(self):
        return Suite.objects.filter(project=self.get_project())

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project)