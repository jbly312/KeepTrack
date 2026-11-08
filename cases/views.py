from django.shortcuts import get_object_or_404
from rest_framework import generics, serializers, permissions
from cases.serializers import SuiteSerializer, TestCaseSerializer
from projects.permissions import ProjectEditorPermission
from projects.models import Project
from cases.models import Suite, TestCase
from django.db import transaction
from projects.mixins import ProjectScopedMixin
# Create your views here.

class SuiteListView(ProjectScopedMixin, generics.ListCreateAPIView, ):
    serializer_class = SuiteSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectEditorPermission]

    def get_queryset(self):
        return Suite.objects.filter(project=self.get_project())

    def perform_create(self, serializer):
        project = self.get_project()
        serializer.save(project=project)

class SuiteDetailView(ProjectScopedMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SuiteSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectEditorPermission]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        return Suite.objects.filter(project=self.get_project())

    def perform_destroy(self, instance):
        if TestCase.objects.filter(suite=instance).exists():
            raise serializers.ValidationError({"suite": "Suite contains test cases (including archived) and can’t be deleted"})
        instance.delete()

class TestCaseListView(ProjectScopedMixin,generics.ListCreateAPIView):
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectEditorPermission]


    def get_queryset(self):
        return TestCase.objects.filter(project=self.get_project(), is_archived=False)

    @transaction.atomic
    def perform_create(self, serializer):
        project = self.get_project()
        suite = serializer.validated_data.get("suite")
        if suite and suite.project != project:
            raise serializers.ValidationError({"suite": "Suite belongs to another project"})
        serializer.save(project=project, created_by=self.request.user)


class TestCaseDetailView(ProjectScopedMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated, ProjectEditorPermission]
    http_method_names = ["get","patch", "delete"]

    def get_queryset(self):
        return TestCase.objects.filter(project=self.get_project(), is_archived=False)

    @transaction.atomic
    def perform_update(self, serializer):
        project = self.get_project()
        suite = serializer.validated_data.get("suite")
        if suite and suite.project != project:
            raise serializers.ValidationError({"suite": "Suite belongs to another project"})
        serializer.save(project=project, created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_archived = True
        instance.save()