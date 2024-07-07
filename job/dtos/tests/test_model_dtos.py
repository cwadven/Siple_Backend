from common.common_testcase_helpers.job.testcase_helpers import create_job_for_testcase
from django.test import (
    TestCase,
)
from job.dtos.model_dtos import (
    ProjectJobAvailabilities,
    ProjectJobRecruitInfo,
)
from project.consts import ProjectRecruitmentStatus


class ProjectJobAvailabilitiesTestCase(TestCase):
    def setUp(self):
        self.job1 = create_job_for_testcase('job1')

    def test_from_recruit_info_when_available(self):
        # Given:
        project_job_recruit_info = ProjectJobRecruitInfo(
            job_id=self.job1.id,
            job_name=self.job1.name,
            job_display_name=self.job1.display_name,
            total_limit=5,
            current_recruited=2,
            recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
        )

        # When:
        project_job_availabilities = ProjectJobAvailabilities.from_recruit_info(project_job_recruit_info)

        # Then:
        self.assertEqual(project_job_availabilities.id, self.job1.id)
        self.assertEqual(project_job_availabilities.display_name, self.job1.display_name)
        self.assertEqual(project_job_availabilities.is_available, True)

    def test_from_recruit_info_when_not_available(self):
        # Given:
        project_job_recruit_info = ProjectJobRecruitInfo(
            job_id=self.job1.id,
            job_name=self.job1.name,
            job_display_name=self.job1.display_name,
            total_limit=5,
            current_recruited=5,
            recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
        )

        # When:
        project_job_availabilities = ProjectJobAvailabilities.from_recruit_info(project_job_recruit_info)

        # Then:
        self.assertEqual(project_job_availabilities.id, self.job1.id)
        self.assertEqual(project_job_availabilities.display_name, self.job1.display_name)
        self.assertEqual(project_job_availabilities.is_available, False)
