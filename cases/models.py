from django.db import models
from projects.models import Project
from django.conf import settings

class Suite(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='suites')
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class TestCase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='testcases')
    suite = models.ForeignKey(Suite, on_delete=models.RESTRICT, null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case #{self.pk}"


class TestCaseVersion(models.Model):
    class Priority(models.TextChoices):
        LOW = 'low', 'LOW'
        MEDIUM = 'medium', 'MEDIUM'
        HIGH = 'high', 'HIGH'
        CRITICAL = 'critical', 'CRITICAL'

    case = models.ForeignKey(TestCase,on_delete= models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    preconditions = models.TextField(blank=True)
    steps = models.JSONField(default=list)
    expected = models.TextField(blank=True)
    priority = models.CharField(choices=Priority.choices,default=Priority.MEDIUM,max_length=10)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['case', 'version_number'], name='unique_case_version'),
        ]

    def __str__(self):
        return f"{self.case} {self.version_number}"