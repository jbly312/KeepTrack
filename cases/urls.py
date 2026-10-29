from django.urls import path
from cases.views import SuiteListView

urlpatterns = [
    path("projects/<int:project_id>/suites/", SuiteListView.as_view(), name = "project-suites")
]