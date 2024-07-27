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
)
from job.services.project_job_services import (
    get_active_job_categories,
    get_active_jobs,
    get_current_active_project_job_recruitments,
    get_current_project_job_availabilities,
)
from member.models import (
    Member,
)
from project.consts import (
    ProjectRecruitmentStatus,
)
from project.models import (
    Project,
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
