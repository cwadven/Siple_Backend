from django.urls import path
from project.views import (
    CreateProjectAPIView,
    GetMyProjectBookmarkAPIView,
    HomeProjectListAPIView,
    ProjectActiveRecruitSelfApplicationAPIView,
    ProjectBookmarkAPIView,
    ProjectDetailAPIView,
    ProjectJobRecruitApplyAPIView,
    ProjectRecruitEligibleAPIView,
)

app_name = 'project'


urlpatterns = [
    path('', CreateProjectAPIView.as_view(), name='project'),

    path(
        '<int:project_id>/active-recruit/applications/self',
        ProjectActiveRecruitSelfApplicationAPIView.as_view(),
        name='project_active_recruit_applications_self',
    ),
    path('<int:project_id>/recruit/job/<int:job_id>/apply', ProjectJobRecruitApplyAPIView.as_view(), name='project_recruit_job_apply'),
    path('<int:project_id>/recruit/eligible', ProjectRecruitEligibleAPIView.as_view(), name='project_recruit_eligible'),
    path('<int:project_id>', ProjectDetailAPIView.as_view(), name='project_detail'),

    path('<int:project_id>/bookmark', ProjectBookmarkAPIView.as_view(), name='project_bookmark'),
    path('my/bookmark', GetMyProjectBookmarkAPIView.as_view(), name='my_project_bookmark'),

    path('home', HomeProjectListAPIView.as_view(), name='home'),
]
