from django.test import TestCase
from job.models import Job
from member.models import Member
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectJobExperienceType,
    ProjectJobSearchOperator,
)
from project.models import (
    Project,
    ProjectCategory,
)
from project.services.project_services import get_filtered_project_qs


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
