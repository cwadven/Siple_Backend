from unittest.mock import (
    MagicMock,
    PropertyMock,
    patch,
)

from common.common_testcase_helpers.job.testcase_helpers import (
    create_job_category_for_testcase,
    create_job_for_testcase,
)
from common.common_testcase_helpers.project.testcase_helpers import (
    create_project_with_active_job_recruitment_for_testcase,
)
from django.test import (
    TestCase,
)
from job.dtos.model_dtos import (
    ProjectJobAvailabilities,
    ProjectJobRecruitInfo,
    RecruitResult,
)
from job.services.project_job_services import (
    ProjectJobRecruitService,
    get_active_job_categories,
    get_active_jobs,
    get_current_active_project_job_recruitments,
    get_current_project_job_availabilities,
)
from member.models import (
    Member,
)
from project.consts import (
    ProjectRecruitApplicationStatus,
    ProjectRecruitmentStatus,
)
from project.models import (
    Project,
    ProjectRecruitApplication,
    ProjectRecruitment,
)


class ProjectJobRecruitmentTestCase(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(username='test', nickname='test')
        self.job_backend = create_job_for_testcase('backend')
        self.job_frontend = create_job_for_testcase('frontend')
        self.project1 = Project.objects.create(title='Project1', created_member_id=self.member.id)
        self.project1_recruitment_job_for_backend = create_project_with_active_job_recruitment_for_testcase(
            project=self.project1,
            job_id=self.job_backend.id,
            created_member_id=self.member.id,
            total_limit=5,
            current_recruited=2,
        )
        self.project1_recruitment_job_for_frontend = create_project_with_active_job_recruitment_for_testcase(
            project=self.project1,
            job_id=self.job_frontend.id,
            created_member_id=self.member.id,
            total_limit=3,
            current_recruited=1,
        )
        self.project2 = Project.objects.create(title='Project2', created_member_id=self.member.id)
        self.project2_recruitment_job_for_backend = create_project_with_active_job_recruitment_for_testcase(
            project=self.project2,
            job_id=self.job_backend.id,
            created_member_id=self.member.id,
            total_limit=2,
            current_recruited=2,
        )
        self.project2_recruitment_job_for_backend.recruit_status = ProjectRecruitmentStatus.RECRUIT_FINISH.value
        self.project2_recruitment_job_for_backend.save()
        self.project2_recruitment_job_for_frontend = create_project_with_active_job_recruitment_for_testcase(
            project=self.project2,
            job_id=self.job_frontend.id,
            created_member_id=self.member.id,
            total_limit=1,
            current_recruited=1,
        )
        self.project2_recruitment_job_for_frontend.recruit_status = ProjectRecruitmentStatus.RECRUIT_FINISH.value
        self.project2_recruitment_job_for_frontend.save()

    def test_get_current_active_project_job_recruitments(self):
        # Given: A list of project IDs
        project_ids = [self.project1.id, self.project2.id]

        # When: We call the function with a list of project IDs
        result = get_current_active_project_job_recruitments(project_ids)

        # Then: We should get a dictionary mapping project IDs to active recruitment jobs, excluding non-recruiting projects
        expected_result = {
            1: [
                ProjectJobRecruitInfo(
                    job_id=self.job_backend.id,
                    job_name=self.job_backend.name,
                    job_display_name=self.job_backend.name,
                    total_limit=5,
                    current_recruited=2,
                    recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
                ),
                ProjectJobRecruitInfo(
                    job_id=self.job_frontend.id,
                    job_name=self.job_frontend.name,
                    job_display_name=self.job_frontend.name,
                    total_limit=3,
                    current_recruited=1,
                    recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
                )
            ],
            2: [
                ProjectJobRecruitInfo(
                    job_id=self.job_backend.id,
                    job_name=self.job_backend.name,
                    job_display_name=self.job_backend.name,
                    total_limit=2,
                    current_recruited=2,
                    recruit_status=ProjectRecruitmentStatus.RECRUIT_FINISH.value,
                ),
                ProjectJobRecruitInfo(
                    job_id=self.job_frontend.id,
                    job_name=self.job_frontend.name,
                    job_display_name=self.job_frontend.name,
                    total_limit=1,
                    current_recruited=1,
                    recruit_status=ProjectRecruitmentStatus.RECRUIT_FINISH.value,
                )
            ]
        }
        self.assertEqual(result, expected_result)

    def test_get_current_active_project_job_recruitments_should_return_empty_dictionary_when_empty_list_send(self):
        # Given: An empty list of project IDs
        project_ids = []

        # When: We call the function with an empty list of project IDs
        result = get_current_active_project_job_recruitments(project_ids)

        # Then: We should get an empty dictionary
        self.assertEqual(result, {})


class GetActiveJobCategoriesTest(TestCase):
    def setUp(self):
        self.valid_category = create_job_category_for_testcase('valid')
        self.hidden_category = create_job_category_for_testcase('hidden')
        self.hidden_category.is_hidden = True
        self.hidden_category.save()
        self.deleted_category = create_job_category_for_testcase('deleted')
        self.deleted_category.is_deleted = True
        self.deleted_category.save()

    def test_get_active_job_categories(self):
        # When: We call the function
        result = get_active_job_categories()

        # Then: We should get a list of active job categories
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.valid_category.id)
        self.assertEqual(result[0].name, 'valid')


class GetActiveJobs(TestCase):
    def setUp(self):
        self.valid_job = create_job_for_testcase('valid')
        self.hidden_job = create_job_for_testcase('hidden')
        self.hidden_job.is_hidden = True
        self.hidden_job.save()
        self.deleted_job = create_job_for_testcase('deleted')
        self.deleted_job.is_deleted = True
        self.deleted_job.save()

    def test_get_active_jobs(self):
        # When: We call the function
        result = get_active_jobs()

        # Then: We should get a list of active jobs
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].id, self.valid_job.id)
        self.assertEqual(result[0].name, 'valid')


class GetCurrentProjectJobAvailabilitiesTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(username='test', nickname='test')
        self.job_backend = create_job_for_testcase('backend')
        self.job_frontend = create_job_for_testcase('frontend')
        self.project = Project.objects.create(title='Project', created_member_id=self.member.id)
        self.project_recruitment_job_for_backend = create_project_with_active_job_recruitment_for_testcase(
            project=self.project,
            job_id=self.job_backend.id,
            created_member_id=self.member.id,
            total_limit=2,
            current_recruited=1,
        )
        self.project_recruitment_job_for_backend.recruit_status = ProjectRecruitmentStatus.RECRUITING.value
        self.project_recruitment_job_for_backend.save()
        self.project_recruitment_job_for_frontend = create_project_with_active_job_recruitment_for_testcase(
            project=self.project,
            job_id=self.job_frontend.id,
            created_member_id=self.member.id,
            total_limit=1,
            current_recruited=1,
        )
        self.project_recruitment_job_for_frontend.recruit_status = ProjectRecruitmentStatus.RECRUIT_FINISH.value
        self.project_recruitment_job_for_frontend.save()

    def test_get_current_project_job_availabilities_with_job_ids_exists(self):
        # Given:
        # When: We call the function with a project ID and a set of job IDs
        result = get_current_project_job_availabilities(
            self.project.id,
            {self.job_backend.id, self.job_frontend.id},
        )

        # Then: The result should only contain availabilities for the specified job IDs
        self.assertEqual(
            result,
            {
                self.job_backend.id: ProjectJobAvailabilities(id=self.job_backend.id, display_name=self.job_backend.display_name, is_available=True),
                self.job_frontend.id: ProjectJobAvailabilities(id=self.job_frontend.id, display_name=self.job_frontend.display_name, is_available=False),
            }
        )

    def test_get_current_project_job_availabilities_with_job_ids_not_exists(self):
        # Given:
        # When: We call the function with a project ID and a set of job IDs
        result = get_current_project_job_availabilities(
            self.project.id,
        )

        # Then: The result should only contain availabilities for the specified all job IDs
        self.assertEqual(
            result,
            {
                self.job_backend.id: ProjectJobAvailabilities(id=self.job_backend.id, display_name=self.job_backend.display_name, is_available=True),
                self.job_frontend.id: ProjectJobAvailabilities(id=self.job_frontend.id, display_name=self.job_frontend.display_name, is_available=False),
            }
        )

    def test_get_current_project_job_availabilities_with_job_ids_specific_exists(self):
        # Given:
        # When: We call the function with a project ID and a set of job IDs
        result = get_current_project_job_availabilities(
            self.project.id,
            {self.job_backend.id},
        )

        # Then: The result should only contain availabilities for the specified job ID
        self.assertEqual(
            result,
            {
                self.job_backend.id: ProjectJobAvailabilities(id=self.job_backend.id, display_name=self.job_backend.display_name, is_available=True),
            }
        )


class ProjectJobRecruitServiceTestCase(TestCase):

    def setUp(self):
        # Given: Create Members
        self.member = Member.objects.create_user(username='test', nickname='test')
        # And: Create Jobs
        self.job_backend = create_job_for_testcase('backend')
        self.job_frontend = create_job_for_testcase('frontend')
        # And: Create project
        self.project = Project.objects.create(title='Project', created_member_id=self.member.id)
        # And: Create ProjectRecruitment
        self.project_recruitment = ProjectRecruitment.objects.create(
            project=self.project,
            times_project_recruit=1,
            recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
            created_member=self.member,
        )
        # And: Set project latest_project_recruitment
        self.project.latest_project_recruitment = self.project_recruitment
        self.project.save()
        # And Create ProjectRecruitmentJob for backend and set it to recruiting
        self.project_recruitment_job_for_backend = create_project_with_active_job_recruitment_for_testcase(
            project=self.project,
            job_id=self.job_backend.id,
            created_member_id=self.member.id,
            total_limit=2,
            current_recruited=1,
        )
        self.project_recruitment_job_for_backend.project_recruitment = self.project_recruitment
        self.project_recruitment_job_for_backend.recruit_status = ProjectRecruitmentStatus.RECRUITING.value
        self.project_recruitment_job_for_backend.save()
        # And Create ProjectRecruitmentJob for frontend and set it to recruited finish
        self.project_recruitment_job_for_frontend = create_project_with_active_job_recruitment_for_testcase(
            project=self.project,
            job_id=self.job_frontend.id,
            created_member_id=self.member.id,
            total_limit=1,
            current_recruited=1,
        )
        self.project_recruitment_job_for_frontend.project_recruitment = self.project_recruitment
        self.project_recruitment_job_for_frontend.recruit_status = ProjectRecruitmentStatus.RECRUIT_FINISH.value
        self.project_recruitment_job_for_frontend.save()
        # And: Add backend to project latest_project_recruitment_jobs
        self.project.latest_project_recruitment_jobs.add(self.job_backend)
        # And: Create ProjectJobRecruitService
        self.service = ProjectJobRecruitService(
            self.project.id,
            self.job_backend.id,
            self.member.id,
        )

    @patch('job.services.project_job_services.Project.objects.get')
    def test_validate_recruit_project_does_not_exist(self,
                                                     mock_project_get):
        # Given: 프로젝트가 존재하지 않는 경우
        mock_project_get.side_effect = Project.DoesNotExist

        # When: validate_recruit 메서드 호출
        result = self.service.validate_recruit()

        # Then: '프로젝트가 존재하지 않습니다.' 메시지와 함께 is_recruited가 False여야 함
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, False)
        self.assertEqual(result.message, '프로젝트가 존재하지 않습니다.')

    def test_validate_recruit_not_recruiting(self):
        # Given: 프로젝트가 존재하지만 모집중이 아닌 경우
        self.project.latest_project_recruitment_id = None
        self.project.save()

        # When: validate_recruit 메서드 호출
        result = self.service.validate_recruit()

        # Then: '아직 모집중이 아닙니다.' 메시지와 함께 is_recruited가 False여야 함
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, False)
        self.assertEqual(result.message, '아직 모집중이 아닙니다.')

    @patch('job.services.project_job_services.ProjectCurrentRecruitStatus.is_recruiting')
    def test_validate_recruit_not_recruiting_by_current_recruit_status(self, mock_is_recruiting):
        # Given: 프로젝트가 current_recruit_status 이슈
        mock_is_recruiting.return_value = False

        # When: validate_recruit 메서드 호출
        result = self.service.validate_recruit()

        # Then: '모집이 마감되었습니다.' 메시지와 함께 is_recruited가 False여야 함
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, False)
        self.assertEqual(result.message, '모집이 마감되었습니다.')
        mock_is_recruiting.assert_called_once()

    def test_validate_recruit_no_job_available(self):
        # Given: 프로젝트가 존재하고 모집중이지만 해당 job이 없는 경우
        self.service.job_id = self.job_frontend.id

        # When: validate_recruit 메서드 호출
        result = self.service.validate_recruit()

        # Then: '모집이 마감되었습니다.' 메시지와 함께 is_recruited가 False여야 함
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, False)
        self.assertEqual(result.message, '모집이 마감되었습니다.')

    def test_validate_recruit_success(self):
        # Given:
        # When: validate_recruit 메서드 호출
        result = self.service.validate_recruit()

        # Then: '지원 가능합니다.' 메시지와 함께 is_recruited가 True여야 함
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, True)
        self.assertEqual(result.message, '지원 가능합니다.')

    @patch('job.services.project_job_services.ProjectJobRecruitService.get_or_create_recruit_application')
    @patch('job.services.project_job_services.ProjectJobRecruitService.validate_recruit')
    def test_recruit_success_with_mocking(self,
                                          mock_validate_recruit,
                                          mock_get_or_create_recruit_application):
        # Given: validate_recruit 메서드가 True를 반환하도록 설정
        mock_validate_recruit.return_value = RecruitResult(is_recruited=True, message='지원 가능합니다.')
        # And: get_or_create_recruit_application 메서드가 RecruitResult를 반환하도록 설정
        mock_get_or_create_recruit_application.return_value = RecruitResult(is_recruited=True, message='지원이 완료되었습니다.')

        # When: validate_recruit 메서드 호출
        result = self.service.recruit('지원 요청 메시지')

        # Then: '지원 가능합니다.' 메시지와 함께 is_recruited가 True여야 함
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, True)
        self.assertEqual(result.message, '지원이 완료되었습니다.')
        mock_get_or_create_recruit_application.assert_called_once_with(
            '지원 요청 메시지'
        )

    @patch('job.services.project_job_services.ProjectJobRecruitService.get_or_create_recruit_application')
    @patch('job.services.project_job_services.ProjectJobRecruitService.validate_recruit')
    def test_recruit_failed_with_mocking_validate_recruit(self,
                                                          mock_validate_recruit,
                                                          mock_get_or_create_recruit_application):
        # Given: validate_recruit 메서드가 False 반환하도록 설정
        mock_validate_recruit.return_value = RecruitResult(is_recruited=False, message='False Test')

        # When: validate_recruit 메서드 호출
        result = self.service.recruit('지원 요청 메시지')

        # Then: '지원 가능합니다.' 메시지와 함께 is_recruited가 True여야 함
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, False)
        self.assertEqual(result.message, 'False Test')
        mock_get_or_create_recruit_application.assert_not_called()

    def test_get_or_create_recruit_application_already_applied(self):
        # Given: 프로젝트와 job이 존재하고, 이미 지원한 경우
        ProjectRecruitApplication.objects.get_or_create(
            project_recruitment_job_id=self.project_recruitment_job_for_backend.id,
            member_id=self.member.id,
            request_status=ProjectRecruitApplicationStatus.IN_REVIEW.value,
            request_message='지원하기.',
        )

        # When: get_or_create_recruit_application 메서드 호출
        result = self.service.get_or_create_recruit_application('지원하기.')

        # Then: '이미 지원한 모집입니다.' 메시지와 함께 is_recruited가 False여야 함
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, False)
        self.assertEqual(result.message, '이미 지원한 모집입니다.')

    def test_get_or_create_recruit_application_success(self):
        # Given: 프로젝트와 job이 존재하고, 지원하지 않은 경우
        # When: get_or_create_recruit_application 메서드 호출
        result = self.service.get_or_create_recruit_application('지원하기.')

        # Then: '지원이 완료되었습니다.' 메시지와 함께 is_recruited
        self.assertIsInstance(result, RecruitResult)
        self.assertEqual(result.is_recruited, True)
        self.assertEqual(result.message, '지원이 완료되었습니다.')

    @patch('job.services.project_job_services.Project.objects.get')
    def test_project_exists(self, mock_project_get):
        # Given: 프로젝트가 존재하는 경우
        mock_project_get.return_value = self.project

        # When: project 속성 접근
        result = self.service.project

        # Then: 반환된 결과가 Project 인스턴스여야 함
        self.assertEqual(result, self.project)
        mock_project_get.assert_called_once_with(id=self.project.id)

    @patch('job.services.project_job_services.Project.objects.get')
    def test_project_does_not_exist(self, mock_project_get):
        # Given: 프로젝트가 존재하지 않는 경우
        mock_project_get.side_effect = Project.DoesNotExist

        # When: project 속성 접근
        result = self.service.project

        # Then: 반환된 결과가 None이어야 함
        self.assertEqual(result, None)
        mock_project_get.assert_called_once_with(id=self.project.id)

    @patch('job.services.project_job_services.get_current_project_job_availabilities')
    def test_current_project_job_availabilities(self, mock_get_current_project_job_availabilities):
        # Given: get_current_project_job_availabilities가 예상된 값을 반환하는 경우
        expected_availability = {self.job_backend.id: MagicMock(spec=ProjectJobAvailabilities)}
        mock_get_current_project_job_availabilities.return_value = expected_availability

        # When: current_project_job_availabilities 속성 접근
        result = self.service.current_project_job_availabilities

        # Then: 반환된 결과가 예상된 값과 동일해야 함
        self.assertEqual(result, expected_availability)
        mock_get_current_project_job_availabilities.assert_called_once_with(self.project.id, {self.job_backend.id})

    @patch('job.services.project_job_services.ProjectRecruitmentJob.objects.filter')
    def test_project_recruitment_job_recruiting(self, mock_project_recruitment_job_filter):
        # Given: 프로젝트가 존재하고 모집중인 job이 있는 경우
        recruitment_job = MagicMock()
        mock_project_recruitment_job_filter.return_value.last.return_value = recruitment_job

        # When: project_recruitment_job_recruiting 속성 접근
        result = self.service.project_recruitment_job_recruiting

        # Then: 반환된 결과가 ProjectRecruitmentJob 인스턴스여야 함
        self.assertEqual(result, recruitment_job)
        mock_project_recruitment_job_filter.assert_called_once_with(
            project_recruitment_id=self.project.latest_project_recruitment_id,
            job_id=self.service.job_id,
            recruit_status=ProjectRecruitmentStatus.RECRUITING.value
        )

    @patch.object(ProjectJobRecruitService, 'current_project_job_availabilities', new_callable=PropertyMock)
    def test_is_job_available_job_not_in_availabilities(self, mock_current_project_job_availabilities):
        # Given: current_project_job_availabilities에 job_id가 없는 경우
        mock_current_project_job_availabilities.return_value = {}

        # When: is_job_available 메서드 호출
        result = self.service.is_job_available()

        # Then: 반환된 결과가 False여야 함
        self.assertEqual(result, False)

    @patch.object(ProjectJobRecruitService, 'current_project_job_availabilities', new_callable=PropertyMock)
    def test_is_job_available_job_is_available(self, mock_current_project_job_availabilities):
        # Given: current_project_job_availabilities에 job_id가 있고 is_available이 True인 경우
        availability = MagicMock(spec=ProjectJobAvailabilities)
        availability.is_available = True
        mock_current_project_job_availabilities.return_value = {self.service.job_id: availability}

        # When: is_job_available 메서드 호출
        result = self.service.is_job_available()

        # Then: 반환된 결과가 True여야 함
        self.assertEqual(result, True)

    @patch.object(ProjectJobRecruitService, 'current_project_job_availabilities', new_callable=PropertyMock)
    def test_is_job_available_job_is_not_available(self, mock_current_project_job_availabilities):
        # Given: current_project_job_availabilities에 job_id가 있고 is_available이 False인 경우
        availability = MagicMock(spec=ProjectJobAvailabilities)
        availability.is_available = False
        mock_current_project_job_availabilities.return_value = {self.service.job_id: availability}

        # When: is_job_available 메서드 호출
        result = self.service.is_job_available()

        # Then: 반환된 결과가 False여야 함
        self.assertEqual(result, False)
