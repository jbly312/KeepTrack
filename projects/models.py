from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    class Role(models.TextChoices):
        OWNER = 'owner' , "Owner"
        EDITOR = 'editor' , "Editor"
        VIEWER = 'viewer' , "Viewer"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(choices=Role.choices,default=Role.VIEWER,max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','project'], name='uniq_project_member'),
        ]

    def __str__(self):
        return f"{self.user} @ {self.project}({self.role})"