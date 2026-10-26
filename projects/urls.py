from django.urls import path
from projects.views import ProjectListView

urlpatterns =  [
    path("projects/", ProjectListView.as_view(), name = 'projects')
]

