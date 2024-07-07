from django.test import TestCase
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectDetailStatus,
    ProjectResultStatus,
    ProjectStatus,
)
from project.models import Project


class ProjectDetailStatusTests(TestCase):
    def test_get_by_project_should_return_recruiting(self):
        # Given: project.current_recruit_status = RECRUITING
        project = Project(
            current_recruit_status=ProjectCurrentRecruitStatus.RECRUITING.value,
        )

        # When: get_by_project 함수 실행
        result = ProjectDetailStatus.get_by_project(project)

        # Then: RECRUITING 반환
        self.assertEqual(result, ProjectDetailStatus.RECRUITING)

    def test_get_by_project_should_return_working(self):
        # Given: project.current_recruit_status = RECRUITED, project.project_status = WORKING
        project = Project(
            current_recruit_status=ProjectCurrentRecruitStatus.RECRUITED.value,
            project_status=ProjectStatus.WORKING.value,
        )

        # When: get_by_project 함수 실행
        result = ProjectDetailStatus.get_by_project(project)

        # Then: WORKING 반환
        self.assertEqual(result, ProjectDetailStatus.WORKING)

    def test_get_by_project_should_return_fail(self):
        # Given: project.current_recruit_status = RECRUITED
        # project.project_result_status = FAIL
        project = Project(
            current_recruit_status=ProjectCurrentRecruitStatus.RECRUITED.value,
            project_status=ProjectStatus.FINISHED.value,
            project_result_status=ProjectResultStatus.FAIL.value,
        )

        # When: get_by_project 함수 실행
        result = ProjectDetailStatus.get_by_project(project)

        # Then: FAIL 반환
        self.assertEqual(result, ProjectDetailStatus.FAIL)

    def test_get_by_project_should_return_done(self):
        # Given: project.current_recruit_status = RECRUITED
        # project.project_result_status = SUCCESS
        project = Project(
            current_recruit_status=ProjectCurrentRecruitStatus.RECRUITED.value,
            project_status=ProjectStatus.FINISHED.value,
            project_result_status=ProjectResultStatus.SUCCESS.value,
        )

        # When: get_by_project 함수 실행
        result = ProjectDetailStatus.get_by_project(project)

        # Then: DONE 반환
        self.assertEqual(result, ProjectDetailStatus.DONE)

    def test_get_by_project_should_return_unknown(self):
        # Given: project.current_recruit_status = ADDITIONAL_RECRUITING
        # project.project_status = FINISHED
        # project.project_result_status = CANCEL
        project = Project(
            current_recruit_status=ProjectCurrentRecruitStatus.ADDITIONAL_RECRUITING.value,
            project_status=ProjectStatus.READY.value,
            project_result_status=ProjectResultStatus.CANCEL.value,
        )

        # When: get_by_project 함수 실행
        result = ProjectDetailStatus.get_by_project(project)

        # Then: UNKNOWN 반환
        self.assertEqual(result, ProjectDetailStatus.UNKNOWN)
