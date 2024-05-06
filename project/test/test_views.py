from unittest.mock import patch

from django.urls import reverse
from member.models import Member
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

    @patch('project.views.get_objects_with_cursor_pagination')
    @patch('project.views.get_member_bookmarked_project_ids')
    def test_get_projects_with_bookmarked_project(self,
                                                  mock_get_member_bookmarked_project_ids,
                                                  mock_get_objects_with_cursor_pagination):
        # Given: Setup return values for mocked services
        mock_get_objects_with_cursor_pagination.return_value = (
            [self.project3, self.project2],
            True,
            'next_cursor_encoded'
        )
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
                        'jobs': [],
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
                        'jobs': [],
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
