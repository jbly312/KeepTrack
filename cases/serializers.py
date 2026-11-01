
from rest_framework import serializers
from cases.models import Suite,TestCase, TestCaseVersion

class SuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suite
        fields = ["id", "name", "created_at"]


class TestCaseVersionSerializer(serializers.ModelSerializer):
    steps = serializers.ListField(child=serializers.CharField(), required=False)
    class Meta:
        model = TestCaseVersion
        fields = ["version_number", "title", "preconditions","steps", "expected", "priority", "created_at"]
        read_only_fields = ["version_number", "created_at"]

class TestCaseSerializer(serializers.ModelSerializer):
    current = TestCaseVersionSerializer(source="latest_version", read_only=True)
    version = TestCaseVersionSerializer(write_only=True)
    class Meta:
        model = TestCase
        fields = ["id","suite", "is_archived", "created_at", "current", "version"]
        read_only_fields = ["is_archived"]

    def create(self, validated_data):
        version_data = validated_data.pop("version")
        case = TestCase.objects.create(**validated_data)
        TestCaseVersion.objects.create(
            case=case,
            version_number=1,
            created_by=case.created_by,
            **version_data,
        )
        return case

    # version это содержимое версии, version_number поле модели

    def update(self, instance, validated_data):
        version_data = validated_data.pop("version", None)
        author = validated_data.pop("created_by", None)

        if "suite" in validated_data:
            instance.suite = validated_data["suite"]
            instance.save()

        if version_data:
            latest = instance.latest_version
            TestCaseVersion.objects.create(
                case=instance,
                version_number= latest.version_number + 1,
                created_by=author,
                title = version_data.get("title", latest.title),
                preconditions = version_data.get("preconditions", latest.preconditions),
                steps = version_data.get("steps", latest.steps),
                expected = version_data.get("expected", latest.expected),
                priority = version_data.get("priority", latest.priority),
            )
        return instance

