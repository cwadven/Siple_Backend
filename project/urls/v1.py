from django.urls import path
from project.views import HomeProjectListAPIView

app_name = 'project'


urlpatterns = [
    path('home', HomeProjectListAPIView.as_view(), name='home'),
]
