from rest_framework import serializers
from cases.models import Suite

class SuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suite
        fields = ["id", "name", "created_at"]
