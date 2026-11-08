from projects.models import Project
from django.shortcuts import get_object_or_404

class ProjectScopedMixin:

    def get_project(self):
        return get_object_or_404(Project,pk = self.kwargs['project_id'], members__user = self.request.user)