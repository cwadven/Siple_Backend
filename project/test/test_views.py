from unittest.mock import patch

from common.common_testcase_helpers.job.testcase_helpers import create_job_for_testcase
from django.urls import reverse
from job.dtos.model_dtos import ProjectJobRecruitInfo
from member.models import Member
from project.consts import ProjectRecruitmentStatus
from project.models import Project
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)


class HomeProjectListAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('project:home')
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        self.member2 = Member.objects.create_user(username='test2', nickname='test2')
        self.project1 = Project.objects.create(
            title='Project 1',
            created_member_id=self.member2.id,
        )
        self.project2 = Project.objects.create(
            title='Project 2',
            created_member_id=self.member2.id,
        )
        self.project3 = Project.objects.create(
            title='Project 3',
            created_member_id=self.member2.id,
        )
        self.job1 = create_job_for_testcase('job1')

    @patch('project.views.get_current_active_project_job_recruitments')
    @patch('project.views.get_objects_with_cursor_pagination')
    @patch('project.views.get_member_bookmarked_project_ids')
    def test_get_projects_with_bookmarked_project(self,
                                                  mock_get_member_bookmarked_project_ids,
                                                  mock_get_objects_with_cursor_pagination,
                                                  mock_get_current_active_project_job_recruitments):
        # Given: Setup return values for mocked services
        mock_get_objects_with_cursor_pagination.return_value = (
            [self.project3, self.project2],
            True,
            'next_cursor_encoded'
        )
        mock_get_current_active_project_job_recruitments.return_value = {
            self.project3.id: [
                ProjectJobRecruitInfo(
                    job_id=self.job1.id,
                    job_name=self.job1.name,
                    job_display_name=self.job1.display_name,
                    total_limit=5,
                    current_recruited=2,
                    recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
                )
            ],
            self.project2.id: [
                ProjectJobRecruitInfo(
                    job_id=self.job1.id,
                    job_name=self.job1.name,
                    job_display_name=self.job1.display_name,
                    total_limit=5,
                    current_recruited=5,
                    recruit_status=ProjectRecruitmentStatus.RECRUIT_FINISH.value,
                )
            ],
        }
        # And: project3 is bookmarked
        mock_get_member_bookmarked_project_ids.return_value = {self.project3.id}

        # When: Make GET request with size 2
        response = self.client.get(self.url, {'size': 2})

        # Then: Verify the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # And: Verify the response data project3 has is_bookmarked True
        self.assertEqual(
            response.json(),
            {
                'data': [
                    {
                        'id': self.project3.id,
                        'title': self.project3.title,
                        'simple_description': self.project3.description[:100],
                        'jobs': [
                            {
                                'id': self.job1.id,
                                'display_name': self.job1.display_name,
                                'is_available': True,
                            }
                        ],
                        'experience': self.project3.job_experience_type,
                        'engagement_level': self.project3.engagement_level,
                        'current_recruit_status': self.project3.current_recruit_status,
                        'image': self.project3.main_image,
                        'is_bookmarked': True,
                    },
                    {
                        'id': self.project2.id,
                        'title': self.project2.title,
                        'simple_description': self.project2.description[:100],
                        'jobs': [
                            {
                                'id': self.job1.id,
                                'display_name': self.job1.display_name,
                                'is_available': False,
                            }
                        ],
                        'experience': self.project2.job_experience_type,
                        'engagement_level': self.project2.engagement_level,
                        'current_recruit_status': self.project2.current_recruit_status,
                        'image': self.project2.main_image,
                        'is_bookmarked': False,
                    },
                ],
                'next_cursor': 'next_cursor_encoded',
                'has_more': True,
            }
        )
