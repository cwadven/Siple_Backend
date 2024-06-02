from common.common_testcase_helpers.job.testcase_helpers import (
    create_job_for_testcase,
)
from common.common_testcase_helpers.project.testcase_helpers import (
    create_project_with_active_job_recruitment_for_testcase,
)
from django.test import (
    TestCase,
)
from job.dtos.model_dtos import (
    ProjectJobRecruitInfo,
)
from job.services.project_job_services import (
    get_current_active_project_job_recruitments,
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
