from django.db import models
from django.conf import settings
from cases.models import TestCaseVersion, TestCase
from projects.models import Project
# Create your models here.

class RunStatus(models.TextChoices):
    UNTESTED = 'untested', "UNTESTED"
    PASSED = 'passed', "PASSED"
    FAILED = 'failed', "FAILED"
    BLOCKED = 'blocked', "BLOCKED"
    SKIPPED = 'skipped', "SKIPPED"

class TestRun(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='runs')
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return  f"{self.name}"

class RunItem(models.Model):
    run = models.ForeignKey(TestRun, on_delete=models.CASCADE, related_name='items')
    case_version = models.ForeignKey(TestCaseVersion, on_delete=models.RESTRICT)
    status = models.CharField(choices= RunStatus.choices, default= RunStatus.UNTESTED, max_length=10)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    case = models.ForeignKey(TestCase, on_delete=models.RESTRICT, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['run', 'case'], name='unique_run_case'),
        ]

    def __str__(self):
        return f"{self.run} {self.case_version}"

    def save(self, **kwargs):
        self.case = self.case_version.case
        super().save(**kwargs)

class ResultLog(models.Model):
    item = models.ForeignKey(RunItem, on_delete=models.CASCADE, related_name='logs')
    status = models.CharField(choices=RunStatus.choices,max_length=10)
    comment = models.TextField(blank=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item} {self.status}"