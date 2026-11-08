from django.urls import path
from cases.views import SuiteListView, TestCaseListView, TestCaseDetailView, SuiteDetailView

urlpatterns = [
    path("projects/<int:project_id>/suites/", SuiteListView.as_view(), name = "project-suites"),
    path("projects/<int:project_id>/cases/", TestCaseListView.as_view(), name="project-cases"),
    path("projects/<int:project_id>/cases/<int:pk>/", TestCaseDetailView.as_view(), name="project-case-detail"),
    path("projects/<int:project_id>/suites/<int:pk>/", SuiteDetailView.as_view(), name="project-suites-detail"),
]