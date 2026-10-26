from django.contrib import admin
from projects.models import Project, ProjectMember


# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner",)
    search_fields = ["name","slug"]

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "role")
    list_filter = ("role",)