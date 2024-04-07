from django.db import models
from member.models import Member
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectEngagementLevel,
    ProjectJobExperienceType,
    ProjectManagementPermissionBehavior,
    ProjectManagementPermissionStatus,
    ProjectRecruitmentStatus,
    ProjectResourceStatus,
    ProjectResultStatus,
    ProjectStatus,
)


class Project(models.Model):
    title = models.CharField(
        max_length=256,
        db_index=True,
        help_text='제목',
        verbose_name='제목',
    )
    description = models.TextField(
        help_text='내용',
        verbose_name='내용',
    )
    current_recruit_status = models.CharField(
        max_length=100,
        default=ProjectCurrentRecruitStatus.RECRUITING.value,
        choices=ProjectCurrentRecruitStatus.choices(),
        help_text='현재 모집 상태',
        verbose_name='현재 모집 상태',
    )
    total_recruitment_time = models.PositiveIntegerField(
        default=1,
        help_text='총 모집 횟수 (추가 모집 포함)',
        verbose_name='총 모집 횟수',
    )
    project_status = models.CharField(
        max_length=100,
        default=ProjectStatus.READY.value,
        choices=ProjectStatus.choices(),
        help_text='진행 상태',
        verbose_name='진행 상태',
    )
    project_result_status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=ProjectResultStatus.choices(),
        help_text='결과 상태',
        verbose_name='결과 상태',
    )
    extra_information = models.TextField(
        null=True,
        blank=True,
        help_text='추가 정보 알림톡 링크 같이',
        verbose_name='추가 정보',
    )
    main_image = models.TextField(
        null=True,
        blank=True,
        help_text='메인 이미지',
        verbose_name='메인 이미지',
    )
    job_experience_type = models.CharField(
        max_length=100,
        choices=ProjectJobExperienceType.choices(),
        help_text='경력 구분',
        verbose_name='경력 구분',
    )
    engagement_level = models.CharField(
        max_length=100,
        choices=ProjectEngagementLevel.choices(),
        help_text='참여도',
        verbose_name='참여도',
    )
    created_member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING,
        related_name='created_projects',
        help_text='생성자',
    )
    resource_status = models.CharField(
        max_length=100,
        default=ProjectResourceStatus.ACTIVE.value,
        help_text='유효 상태',
        verbose_name='유효 상태',
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='삭제 일시',
        verbose_name='삭제 일시',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='생성 일시',
        verbose_name='생성 일시',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='수정 일시',
        verbose_name='수정 일시',
    )
    rearrangement_time = models.DateTimeField(
        help_text='정렬 기준 시간',
        verbose_name='정렬 기준 시간',
        db_index=True,
    )
    project_start_time = models.DateTimeField(
        help_text='시작 시간',
        verbose_name='시작 시간',
        db_index=True,
    )
    project_end_time = models.DateTimeField(
        help_text='종료 시간',
        verbose_name='종료 시간',
        db_index=True,
    )

    def __str__(self):
        return self.title


class ProjectDuration(models.Model):
    display_name = models.CharField(
        max_length=256,
        help_text='표시명',
    )
    name = models.CharField(
        max_length=256,
        help_text='명칭',
        db_index=True,
    )
    description = models.TextField(
        help_text='설명',
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text='삭제 여부',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='생성 일시',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='수정 일시',
    )

    def __str__(self):
        return f'{self.display_name} - {self.name} - {self.is_deleted}'


class ProjectManagementPermission(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.DO_NOTHING,
        help_text='프로젝트',
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING,
        help_text='멤버',
    )
    permission = models.CharField(
        max_length=100,
        help_text='권한',
        choices=ProjectManagementPermissionBehavior.choices(),
    )
    status = models.CharField(
        max_length=100,
        help_text='상태',
        choices=ProjectManagementPermissionStatus.choices(),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='생성 일시',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='수정 일시',
    )

    def __str__(self):
        return f'{self.project_id} - {self.member_id} - {self.permission}'


class ProjectRecruitment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.DO_NOTHING,
        help_text='프로젝트',
    )
    times_project_recruit = models.PositiveIntegerField(
        db_index=True,
        help_text='모집 횟수 (처음 생성 시 1, 추가 모집 시 Project recruitment_time + 1)',
    )
    recruit_status = models.CharField(
        max_length=100,
        default=ProjectRecruitmentStatus.RECRUITING.value,
        choices=ProjectRecruitmentStatus.choices(),
    )
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )
    created_member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING,
        help_text='생성자',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='생성 일시',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='수정 일시',
    )

    def __str__(self):
        return f'{self.project_id} - {self.recruit_status} - {self.times_project_recruit}'
