from django.contrib import admin
from cases.models import Suite, TestCase, TestCaseVersion


@admin.register(Suite)
class SuiteAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "created_at")
    search_fields = ("name", "project__name")


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "suite", "is_archived")
    list_filter = ("is_archived",)
    search_fields = ("project__name", "suite__name")


@admin.register(TestCaseVersion)
class TestCaseVersionAdmin(admin.ModelAdmin):
    list_display = ("case", "version_number", "title", "priority")
    list_filter = ("priority",)
    search_fields = ("title", )