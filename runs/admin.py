from django.contrib import admin
from runs.models import TestRun, ResultLog, RunItem
# Register your models here.
@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "created_at", "closed_at")
    search_fields = ("name", "project__name")

@admin.register(RunItem)
class RunItemAdmin(admin.ModelAdmin):
    list_display = ("run", "case", "case_version", "status", "assignee")
    list_filter = ("status",)
    readonly_fields = ("case",)
    search_fields =  ("run__name", "case_version__title")

@admin.register(ResultLog)
class ResultLogAdmin(admin.ModelAdmin):
    list_display = ("item", "status", "changed_by" ,"created_at")
    list_filter = ("status",)
    search_fields = ("item__run__name",  "item__case_version__title")
