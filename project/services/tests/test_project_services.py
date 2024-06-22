from common.common_testcase_helpers.job.testcase_helpers import create_job_for_testcase
from django.test import TestCase
from job.models import Job
from member.models import Member
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectJobExperienceType,
    ProjectJobSearchOperator,
    ProjectManagementPermissionBehavior,
)
from project.dtos.request_dtos import CreateProjectJob
from project.models import (
    Project,
    ProjectCategory,
    ProjectManagementPermission,
    ProjectRecruitApplication,
    ProjectRecruitment,
    ProjectRecruitmentJob,
)
from project.services.project_services import (
    create_project_management_permissions,
    create_project_member_management,
    create_project_recruitment_and_update_project,
    create_project_recruitment_jobs,
    get_filtered_project_qs,
    get_maximum_project_recruit_times,
)


class ProjectFilterTestCase(TestCase):
    def setUp(self):
        # Create some categories
        self.category1 = ProjectCategory.objects.create(
            display_name='재미/흥미',
            name='FUN'
        )
        self.category2 = ProjectCategory.objects.create(
            display_name='재테크',
            name='EARN',
        )

        # Create some Member
        self.member = Member.objects.create_user(username='test')

        # Create some jobs
        self.backend_job = Job.objects.create(
            display_name='백엔드',
            name='backend',
        )
        self.frontend_job = Job.objects.create(
            display_name='프론트엔드',
            name='frontend',
        )
        self.devops_job = Job.objects.create(
            display_name='데브옵스',
            name='devops',
        )

        # Create some projects
        self.project1 = Project.objects.create(
            title='Test Project 1',
            category=self.category1,
            job_experience_type=ProjectJobExperienceType.ALL.value,
            current_recruit_status=ProjectCurrentRecruitStatus.RECRUITING.value,
            hours_per_week=10,
            duration_month=6,
            created_member=self.member,
            is_deleted=False,
        )
        self.project1.latest_project_recruitment_jobs.set([self.backend_job, self.devops_job, self.frontend_job])

        self.project2 = Project.objects.create(
            title='Another Project',
            category=self.category2,
            job_experience_type=ProjectJobExperienceType.ALL.value,
            current_recruit_status=ProjectCurrentRecruitStatus.RECRUITED.value,
            hours_per_week=20,
            duration_month=12,
            created_member=self.member,
            is_deleted=False,
        )
        self.project2.latest_project_recruitment_jobs.set([self.frontend_job])

    def test_filter_by_title(self):
        # Given: Title filter
        title = 'Test'

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=title,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Only project with title starting with 'Test' should be returned
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_category(self):
        # Given: Category filter
        category_ids = [self.project1.category.id]

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=category_ids,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Only project with the given category should be returned
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_job_ids_or(self):
        # Given: Job ID filter with OR operator but only one has to match
        job_ids = [self.project2.latest_project_recruitment_jobs.first().id, self.devops_job.id]
        jobs_operator = ProjectJobSearchOperator.OR.value

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=job_ids,
            jobs_operator=jobs_operator,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects that match any of the job IDs should be returned
        self.assertEqual(qs.count(), 2)
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_job_ids_and(self):
        # Given: Job ID filter with AND operator
        job_ids = [self.devops_job.id, self.backend_job.id, self.frontend_job.id]
        jobs_operator = ProjectJobSearchOperator.AND.value

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=job_ids,
            jobs_operator=jobs_operator,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects that match any of the job IDs should be returned
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_experience(self):
        # Given: Experience filter
        experience = ProjectJobExperienceType.ALL.value

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=experience,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects with the given experience should be returned
        self.assertEqual(qs.count(), 2)

    def test_filter_by_current_recruit_status_when_status_recruiting(self):
        # Given: Current recruit status filter
        current_recruit_status = ProjectCurrentRecruitStatus.RECRUITING.value

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=current_recruit_status
        )

        # Then: Only recruiting projects should be returned
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_current_recruit_status_when_status_additional_recruiting(self):
        # Given: Current recruit status ADDITIONAL_RECRUITING
        self.project1.current_recruit_status = ProjectCurrentRecruitStatus.ADDITIONAL_RECRUITING.value
        self.project1.save()
        current_recruit_status = ProjectCurrentRecruitStatus.RECRUITING.value

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=current_recruit_status
        )

        # Then: Only recruiting projects should be returned
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_current_recruit_status_when_status_recruited(self):
        # Given: Current recruit status RECRUITED
        current_recruit_status = ProjectCurrentRecruitStatus.RECRUITED.value

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=current_recruit_status
        )

        # Then: Only recruiting projects should be returned
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.project2)

    def test_filter_by_min_and_max_hours_per_week_with_both_value(self):
        # Given: Min and max hours per week filter
        min_hours_per_week = 5
        max_hours_per_week = 15

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=min_hours_per_week,
            max_hours_per_week=max_hours_per_week,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects within the given hours per week range should be returned
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_min_and_max_hours_per_week_with_min_value(self):
        # Given: Min hours per week filter
        min_hours_per_week = 15

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=min_hours_per_week,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects within the given hours per week range should be returned
        self.assertEqual(qs.count(), 1)
        # And: return project 2 due to hours_per_week is bigger than max_hours_per_week
        self.assertEqual(qs.first(), self.project2)

    def test_filter_by_min_and_max_hours_per_week_with_max_value(self):
        # Given: Max hours per week filter
        max_hours_per_week = 15

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=max_hours_per_week,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects within the given hours per week range should be returned
        self.assertEqual(qs.count(), 1)
        # And: return project 1 due to hours_per_week is lower than max_hours_per_week
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_min_and_max_hours_per_week_with_max_value_and_null_value_project(self):
        # Given: Max hours per week filter
        max_hours_per_week = 15
        # And: Set project1 hours_per_week to None
        self.project1.hours_per_week = None
        self.project1.save()

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=max_hours_per_week,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects within the given hours per week range should be returned
        self.assertEqual(qs.count(), 1)
        # And: return project 1 due to hours_per_week is null
        # And: project 2 is 20 hours_per_week
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_min_and_max_hours_per_week_with_min_value_and_null_value_project(self):
        # Given: Min hours per week filter
        min_hours_per_week = 30
        # And: Set project1 hours_per_week to None
        self.project1.hours_per_week = None
        self.project1.save()

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=min_hours_per_week,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects within the given hours per week range should be returned
        self.assertEqual(qs.count(), 1)
        # And: return project 1 due to hours_per_week is null
        # And: project 2 is 20 hours_per_week
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_min_and_max_duration_month_with_both_value(self):
        # Given: Min and max duration month filter
        min_duration_month = 5
        max_duration_month = 7

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=min_duration_month,
            max_duration_month=max_duration_month,
            current_recruit_status=None
        )

        # Then: Projects within the given duration month range should be returned
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_min_and_max_duration_month_with_min_value(self):
        # Given: Min duration month filter
        min_duration_month = 10

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=min_duration_month,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects within the given duration month range should be returned
        self.assertEqual(qs.count(), 1)
        # And: return project 2 due to duration_month is bigger than min_duration_month
        self.assertEqual(qs.first(), self.project2)

    def test_filter_by_min_and_max_duration_month_with_max_value(self):
        # Given: Max duration month filter
        max_duration_month = 7

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=max_duration_month,
            current_recruit_status=None
        )

        # Then: Projects within the given duration month range should be returned
        self.assertEqual(qs.count(), 1)
        # And: return project 1 due to duration_month is lower than max_duration_month
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_min_and_max_duration_month_with_max_value_and_null_value_project(self):
        # Given: Max duration month filter
        max_duration_month = 7
        # And: Set project1 duration_month to None
        self.project1.duration_month = None
        self.project1.save()

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=None,
            max_duration_month=max_duration_month,
            current_recruit_status=None
        )

        # Then: Projects within the given duration_month range should be returned
        self.assertEqual(qs.count(), 1)
        # And: return project 1 due to duration_month is null
        # And: project 2 is 12 duration_month
        self.assertEqual(qs.first(), self.project1)

    def test_filter_by_min_and_max_duration_month_with_min_value_and_null_value_project(self):
        # Given: Min duration month filter
        min_duration_month = 30
        # And: Set project1 duration_month to None
        self.project1.duration_month = None
        self.project1.save()

        # When: Filtering projects
        qs = get_filtered_project_qs(
            title=None,
            category_ids=None,
            job_ids=None,
            jobs_operator=None,
            experience=None,
            min_hours_per_week=None,
            max_hours_per_week=None,
            min_duration_month=min_duration_month,
            max_duration_month=None,
            current_recruit_status=None
        )

        # Then: Projects within the given duration_month range should be returned
        self.assertEqual(qs.count(), 1)
        # And: return project 1 due to duration_month is null
        # And: project 2 is 12 duration_month
        self.assertEqual(qs.first(), self.project1)


class CreateProjectMemberManagementTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(username='test', nickname='test')
        self.project = Project.objects.create(
            title='Project',
            created_member_id=self.member.id,
        )
        self.project_recruitment = ProjectRecruitment.objects.create(
            project=self.project,
            times_project_recruit=1,
            created_member_id=self.member.id,
        )
        self.job_backend = create_job_for_testcase('backend')
        self.project_recruitment_job = ProjectRecruitmentJob.objects.create(
            project_recruitment=self.project_recruitment,
            job=self.job_backend,
            total_limit=10,
            created_member_id=self.member.id,
        )
        self.project_recruit_application = ProjectRecruitApplication.objects.create(
            project_recruitment_job=self.project_recruitment_job,
            member_id=self.member.id,
            request_message='Test',
        )

    def test_create_project_member_management_should_return_is_leader_true_when_param_is_true(self):
        # Given: is_leader is True
        # When:
        project_member_management = create_project_member_management(self.project, is_leader=True)

        # Then: is_leader should be True
        self.assertEqual(project_member_management.project.id, self.project.id)
        self.assertEqual(project_member_management.is_leader, True)

    def test_create_project_member_management_should_return_project_recruit_application_none_when_param_not_exists(self):
        # Given: project_recruit_application is not exists
        # When:
        project_member_management = create_project_member_management(self.project, is_leader=True)

        # Then: project_recruit_application should be None
        self.assertEqual(project_member_management.project.id, self.project.id)
        self.assertEqual(project_member_management.project_recruit_application, None)

    def test_create_project_member_management_should_return_project_recruit_application_when_param_exists(self):
        # Given: project_recruit_application is exists
        # When:
        project_member_management = create_project_member_management(
            self.project,
            is_leader=False,
            project_recruit_application=self.project_recruit_application
        )

        # Then: project_recruit_application should be exists
        self.assertEqual(project_member_management.project.id, self.project.id)
        self.assertEqual(project_member_management.project_recruit_application.id, self.project_recruit_application.id)


class CreateProjectManagementPermissionsTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(username='test', nickname='test')
        self.project = Project.objects.create(
            title='Project',
            created_member_id=self.member.id,
        )

    def test_create_project_management_permissions(self):
        # Given: project_management_permissions
        permissions = [
            ProjectManagementPermissionBehavior(value)
            for value, _ in ProjectManagementPermissionBehavior.choices()
        ]

        # When: create_project_management_permissions
        create_project_management_permissions(
            self.project,
            self.member.id,
            permissions,
        )

        # Then: project_management_permissions should be created
        self.assertEqual(
            ProjectManagementPermission.objects.filter(
                project_id=self.project.id,
                member_id=self.member.id,
            ).count(),
            len(permissions),
        )
        self.assertEqual(
            set(
                ProjectManagementPermission.objects.filter(
                    project_id=self.project.id,
                    member_id=self.member.id,
                ).values_list('permission', flat=True)
            ),
            set(permission.value for permission in permissions),
        )


class TestGetMaximumProjectRecruitTimes(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(username='test', nickname='test')
        self.project = Project.objects.create(
            title='Project',
            created_member_id=self.member.id,
        )
        self.project_recruitment1 = ProjectRecruitment.objects.create(
            project=self.project,
            times_project_recruit=1,
            created_member_id=self.member.id,
        )
        self.project_recruitment2 = ProjectRecruitment.objects.create(
            project=self.project,
            times_project_recruit=2,
            created_member_id=self.member.id,
        )
        self.project_recruitment3 = ProjectRecruitment.objects.create(
            project=self.project,
            times_project_recruit=3,
            created_member_id=self.member.id,
        )

    def test_get_maximum_project_recruit_times(self):
        # Given: project_recruitments with times_project_recruit 1, 2, 3
        # When: get_maximum_project_recruit_times
        max_times_project_recruit = get_maximum_project_recruit_times(self.project)

        # Then: max_times_project_recruit should be 3
        self.assertEqual(max_times_project_recruit, 3)


class CreateProjectRecruitmentTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(username='test', nickname='test')
        self.project = Project.objects.create(
            title='Project',
            created_member_id=self.member.id,
        )

    def test_create_project_recruitment_should_create_times_project_recruit_1_when_not_exists(self):
        # Given: ProjectRecruitment not exists
        ProjectRecruitment.objects.all().delete()

        # When: create_project_recruitment
        project_recruitment = create_project_recruitment_and_update_project(self.project, self.member.id)

        # Given: times_project_recruit should be 1
        self.assertEqual(project_recruitment.project.id, self.project.id)
        self.assertEqual(project_recruitment.times_project_recruit, 1)
        # And: created_member should be member
        self.assertEqual(project_recruitment.created_member.id, self.member.id)
        # And: project latest_project_recruitment should be project_recruitment
        self.assertEqual(self.project.latest_project_recruitment.id, project_recruitment.id)

    def test_create_project_recruitment_should_create_times_project_recruit_as_maximum_when_exists(self):
        # Given: ProjectRecruitment exists
        ProjectRecruitment.objects.create(
            project=self.project,
            times_project_recruit=3,
            created_member_id=self.member.id,
        )

        # When: create_project_recruitment
        project_recruitment = create_project_recruitment_and_update_project(self.project, self.member.id)

        # Given: times_project_recruit should be 4
        self.assertEqual(project_recruitment.times_project_recruit, 4)
        # And: project latest_project_recruitment should be project_recruitment
        self.assertEqual(self.project.latest_project_recruitment.id, project_recruitment.id)


class CreateProjectRecruitmentJobsTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create_user(username='test', nickname='test')
        self.project = Project.objects.create(
            title='Project',
            created_member_id=self.member.id,
        )
        self.project_recruitment = ProjectRecruitment.objects.create(
            project=self.project,
            times_project_recruit=1,
            created_member_id=self.member.id,
        )

    def test_create_project_recruitment_jobs(self):
        # Given: jobs
        job_backend = create_job_for_testcase('backend')
        job_frontend = create_job_for_testcase('frontend')
        # And: Delete ProjectRecruitmentJob
        ProjectRecruitmentJob.objects.all().delete()

        # When: create_project_recruitment_jobs
        create_project_recruitment_jobs(
            [
                CreateProjectJob(job_id=job_backend.id, total_limit=10),
                CreateProjectJob(job_id=job_frontend.id, total_limit=20),
            ],
            self.project_recruitment,
            self.member.id,
        )

        # Then: project_recruitment_jobs should be created
        self.assertEqual(
            ProjectRecruitmentJob.objects.filter(project_recruitment=self.project_recruitment).count(),
            2,
        )
        # And: project_recruitment_jobs should be created with total_limit 10, 20
        self.assertEqual(
            ProjectRecruitmentJob.objects.get(
                project_recruitment=self.project_recruitment,
                job=job_backend
            ).total_limit,
            10,
        )
        self.assertEqual(
            ProjectRecruitmentJob.objects.get(
                project_recruitment=self.project_recruitment,
                job=job_frontend
            ).total_limit,
            20,
        )
