from rest_framework import serializers
from projects.models import Project, ProjectMember
from users.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "slug","owner", "created_at"]
        read_only_fields = ["owner", "created_at"]


class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    user_email = serializers.EmailField(write_only=True)

    class Meta:
        model = ProjectMember
        fields = ["id", "user", "email", "user_email", "role"]
        read_only_fields = ["user"]

    def validate(self, attrs):
        email = attrs.pop("user_email", None)
        if email:
            try:
                attrs["user"] = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({"user_email": "User does not exist"})
        return attrs





