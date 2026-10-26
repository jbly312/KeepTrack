from rest_framework import serializers
from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "slug","owner", "created_at"]
        read_only_fields = ["owner", "created_at"]
