from datetime import datetime
from unittest.mock import (
    MagicMock,
    patch,
)

from common.common_consts.common_error_messages import (
    ErrorMessage,
    InvalidInputResponseErrorStatus,
)
from common.common_testcase_helpers.job.testcase_helpers import create_job_for_testcase
from common.common_utils.error_utils import generate_pydantic_error_detail
from django.urls import reverse
from job.dtos.model_dtos import ProjectJobRecruitInfo
from member.exceptions import LoginRequiredException
from member.models import Member
from project.consts import (
    ProjectJobExperienceType,
    ProjectJobSearchOperator,
    ProjectRecruitmentStatus,
)
from project.dtos.request_dtos import (
    CreateProjectJob,
    CreateProjectRequest,
)
from project.dtos.service_dtos import ProjectCreationData
from project.models import (
    Project,
    ProjectCategory,
    ProjectRecruitment,
)
from pydantic import ValidationError
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
        self.category = ProjectCategory.objects.create(
            display_name='카테고리 테스트',
            name='category_test',
        )
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
            category=self.category,
            hours_per_week=10,
            created_member_id=self.member2.id,
        )
        self.project3_recruitment = ProjectRecruitment.objects.create(
            project_id=self.project3.id,
            times_project_recruit=1,
            recruit_status=ProjectRecruitmentStatus.RECRUIT_FINISH.value,
            created_member_id=self.member2.id,
        )
        self.project3_recruitment.created_at = datetime(2021, 1, 1, 10, 0, 0)
        self.project3_recruitment.save()
        self.job1 = create_job_for_testcase('job1')

    @patch('project.views.get_current_active_project_job_recruitments')
    @patch('project.views.get_objects_with_cursor_pagination')
    @patch('project.views.get_member_bookmarked_project_ids')
    @patch('project.views.get_filtered_project_qs')
    def test_get_projects_with_bookmarked_project(self,
                                                  mock_get_filtered_project_qs,
                                                  mock_get_member_bookmarked_project_ids,
                                                  mock_get_objects_with_cursor_pagination,
                                                  mock_get_current_active_project_job_recruitments):
        # Given: Setup return values for mocked filtered project qs
        mock_get_filtered_project_qs.return_value = [self.project3, self.project2]
        # And: Setup return values for mocked services
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

        # Then: Verify the mocked services are called
        mock_get_filtered_project_qs.assert_called_once_with(
            title=None,
            category_ids=[],
            job_ids=[],
            jobs_operator=ProjectJobSearchOperator.OR.value,
            experience=ProjectJobExperienceType.ALL.value,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None,
        )
        # And: Verify the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # And: Verify the response data project3 has is_bookmarked True
        self.assertDictEqual(
            response.json(),
            {
                'data': [
                    {
                        'id': self.project3.id,
                        'title': self.project3.title,
                        'category_display_name': self.category.display_name,
                        'simple_description': self.project3.description[:100],
                        'jobs': [
                            {
                                'id': self.job1.id,
                                'display_name': self.job1.display_name,
                                'is_available': True,
                            }
                        ],
                        'experience': self.project3.job_experience_type,
                        'hours_per_week': 10,
                        'current_recruit_status': self.project3.current_recruit_status,
                        'image': self.project3.main_image,
                        'is_bookmarked': True,
                        'recent_recruited_at': '2021-01-01T01:00:00Z',
                    },
                    {
                        'id': self.project2.id,
                        'category_display_name': None,
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
                        'hours_per_week': None,
                        'current_recruit_status': self.project2.current_recruit_status,
                        'image': self.project2.main_image,
                        'is_bookmarked': False,
                        'recent_recruited_at': None,
                    },
                ],
                'next_cursor': 'next_cursor_encoded',
                'has_more': True,
            }
        )

    def test_get_projects_should_raise_error_when_request_param_is_invalid(self):
        # Given: Invalid Param error
        data = {
            'size': 2,
            'category_ids': '1,2,invalid_category_id',
        }
        # When: Make GET request with error param
        response = self.client.get(self.url, data)

        # Then: Error 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # And: Error info
        self.assertDictEqual(
            response.json(),
            {
                'message': InvalidInputResponseErrorStatus.INVALID_INPUT_HOME_LIST_PARAM_ERROR_400.label,
                'error_code': InvalidInputResponseErrorStatus.INVALID_INPUT_HOME_LIST_PARAM_ERROR_400.value,
                'errors': {
                    'category_ids': [ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label],
                }
            }
        )


class CreateProjectAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('project:project')
        self.member = Member.objects.create_user(username='test1', nickname='test1')
        self.category = ProjectCategory.objects.create(
            display_name='카테고리 테스트',
            name='category_test',
        )
        self.job1 = create_job_for_testcase('job1')
        self.request_data = {
            'title': 'Test Project',
            'description': 'This is a test project.',
            'category_id': self.category.id,
            'extra_information': 'Extra',
            'image': 'path/to/image.png',
            'experience': 'ALL',
            'hours_per_week': 40,
            'duration_month': 6,
            'jobs': [
                {"job_id": self.job1.id, "total_limit": 5},
            ]
        }

    def test_create_project_should_fail_due_to_not_logged_in(self):
        # Given: Not logged in
        self.client.logout()

        # When: Make POST request
        response = self.client.post(
            self.url,
            self.request_data,
            format='json',
        )

        # Then: Error 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # And: Error info
        self.assertDictEqual(
            response.json(),
            {
                'message': LoginRequiredException.default_detail,
                'error_code': LoginRequiredException.default_code,
                'errors': None,
            }
        )

    @patch('project.views.CreateProjectRequest.of')
    def test_create_project_should_fail_when_invalid_input(self, mock_of):
        # Given: Login
        self.client.force_login(self.member)
        # And: Mock CreateProjectRequest.of
        mock_of.side_effect = ValidationError.from_exception_data(
            title=CreateProjectRequest.__name__,
            line_errors=[
                generate_pydantic_error_detail(
                    'Error',
                    '에러',
                    'extra_information',
                    'ALL',
                )
            ]
        )

        # When: Make POST request
        response = self.client.post(
            self.url,
            self.request_data,
            format='json',
        )

        # Then: Verify the response status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'],
            InvalidInputResponseErrorStatus.INVALID_PROJECT_CREATION_INPUT_DATA_ERROR_400.label,
        )
        self.assertEqual(
            response.data['error_code'],
            InvalidInputResponseErrorStatus.INVALID_PROJECT_CREATION_INPUT_DATA_ERROR_400.value,
        )
        self.assertEqual(
            response.data['errors']['extra_information'],
            ['에러'],
        )

    @patch('project.views.ProjectCreationService')
    def test_create_project_success(self, mock_project_creation_service):
        # Given: Login
        self.client.force_login(self.member)
        # And: Mock ProjectCreationService
        mock_service_instance = mock_project_creation_service.return_value
        mock_project = MagicMock()
        mock_project.id = 1
        mock_service_instance.generate_project.return_value = mock_project

        # When: Make POST request
        response = self.client.post(
            self.url,
            self.request_data, format='json',
        )

        # Then: Verify the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], mock_project.id)
        mock_project_creation_service.assert_called_once_with(
            self.member.id,
            ProjectCreationData(
                title=self.request_data['title'],
                description=self.request_data['description'],
                category_id=self.request_data['category_id'],
                extra_information=self.request_data['extra_information'],
                main_image=self.request_data['image'],
                job_experience_type=self.request_data['experience'],
                hours_per_week=self.request_data['hours_per_week'],
                duration_month=self.request_data['duration_month'],
                jobs=[
                    CreateProjectJob(job_id=job_info['job_id'], total_limit=job_info['total_limit'])
                    for job_info in self.request_data['jobs']
                ]
            )
        )
        mock_service_instance.generate_project.assert_called_once()
