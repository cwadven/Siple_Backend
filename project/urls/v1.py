from django.urls import path
from project.views import (
    CreateProjectAPIView,
    HomeProjectListAPIView,
    ProjectDetailAPIView,
    ProjectJobRecruitApplyAPIView,
    ProjectRecruitEligibleAPIView,
)

app_name = 'project'


urlpatterns = [
    path('', CreateProjectAPIView.as_view(), name='project'),

    path('<int:project_id>/recruit/job/<int:job_id>/apply', ProjectJobRecruitApplyAPIView.as_view(), name='project_recruit_job_apply'),
    path('<int:project_id>/recruit/eligible', ProjectRecruitEligibleAPIView.as_view(), name='project_recruit_eligible'),
    path('<int:project_id>', ProjectDetailAPIView.as_view(), name='project_detail'),

    path('home', HomeProjectListAPIView.as_view(), name='home'),
]
