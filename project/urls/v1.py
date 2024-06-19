from django.urls import path
from project.views import (
    CreateProjectAPIView,
    HomeProjectListAPIView,
)

app_name = 'project'


urlpatterns = [
    path('', CreateProjectAPIView.as_view(), name='project'),
    path('home', HomeProjectListAPIView.as_view(), name='home'),
]
