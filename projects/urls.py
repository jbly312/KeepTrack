from django.urls import path
from projects.views import ProjectListView, ProjectDetailView, ProjectMemberListView, ProjectMemberDetailView

urlpatterns =  [
    path("projects/", ProjectListView.as_view(), name = 'projects'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name = 'projects_detail'),
    path("projects/<int:project_id>/members/", ProjectMemberListView.as_view(), name="project-members"),
    path("projects/<int:project_id>/members/<int:user_id>/", ProjectMemberDetailView.as_view(),name="project-member-detail"),
]

