from django.urls import path
from project.views import (
    CreateProjectAPIView,
    HomeProjectListAPIView,
    ProjectDetailAPIView,
)

app_name = 'project'


urlpatterns = [
    path('', CreateProjectAPIView.as_view(), name='project'),
    path('<int:project_id>', ProjectDetailAPIView.as_view(), name='project_detail'),
    path('home', HomeProjectListAPIView.as_view(), name='home'),
]
