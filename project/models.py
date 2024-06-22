from django.db import models
from member.models import Member
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectJobExperienceType,
    ProjectManagementPermissionBehavior,
    ProjectManagementPermissionStatus,
    ProjectMemberManagementLeftStatus,
    ProjectRecruitApplicationStatus,
    ProjectRecruitmentStatus,
    ProjectResourceStatus,
    ProjectResultStatus,
    ProjectStatus,
)


class ProjectCategory(models.Model):
    display_name = models.CharField(
        max_length=256,
        help_text='표시명',
        verbose_name='표시명',
    )
    name = models.CharField(
        max_length=256,
        help_text='카테고리명',
        verbose_name='카테고리명',
    )
    description = models.TextField(
        help_text='설명',
        verbose_name='설명',
        null=True,
        blank=True,
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text='삭제 여부',
        verbose_name='삭제 여부',
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

    def __str__(self):
        return self.name


class Project(models.Model):
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.DO_NOTHING,
        help_text='카테고리',
        verbose_name='카테고리',
        null=True,
        blank=True,
    )
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
    hours_per_week = models.PositiveIntegerField(
        help_text='주당 참여 시간',
        verbose_name='주당 참여 시간',
        db_index=True,
        null=True,
        blank=True,
    )
    duration_month = models.PositiveIntegerField(
        help_text='프로젝트 기간(월)',
        verbose_name='프로젝트 기간(월)',
        db_index=True,
        null=True,
        blank=True,
    )
    bookmark_count = models.PositiveIntegerField(
        default=0,
        help_text='북마크 수',
        verbose_name='북마크 수',
        db_index=True,
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text='삭제 여부',
        verbose_name='삭제 여부',
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='삭제 일시',
        verbose_name='삭제 일시',
    )
    latest_project_recruitment = models.ForeignKey(
        'ProjectRecruitment',
        related_name='latest_project_recruitment',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        help_text='최신 프로젝트 모집',
        verbose_name='최신 프로젝트 모집',
    )
    latest_project_recruitment_jobs = models.ManyToManyField(
        'job.Job',
        related_name='latest_project_recruitment_jobs',
        help_text='최신 프로젝트 모집 직무들',
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
        auto_now_add=True,
        help_text='정렬 기준 시간',
        verbose_name='정렬 기준 시간',
        db_index=True,
    )
    project_start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='시작 시간',
        verbose_name='시작 시간',
        db_index=True,
    )
    project_end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='종료 시간',
        verbose_name='종료 시간',
        db_index=True,
    )

    def __str__(self):
        return self.title


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


class ProjectRecruitmentJob(models.Model):
    project_recruitment = models.ForeignKey(
        ProjectRecruitment,
        on_delete=models.DO_NOTHING,
        help_text='프로젝트 모집',
    )
    job = models.ForeignKey(
        'job.Job',
        on_delete=models.DO_NOTHING,
        help_text='직무',
    )
    total_limit = models.PositiveIntegerField(
        help_text='총 제한 인원',
        db_index=True,
    )
    current_recruited = models.PositiveIntegerField(
        help_text='현재 모집 인원',
        default=0,
        db_index=True,
    )
    recruit_status = models.CharField(
        max_length=100,
        default=ProjectRecruitmentStatus.RECRUITING.value,
        choices=ProjectRecruitmentStatus.choices(),
        help_text='모집 상태',
    )
    created_member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING,
        help_text='생성자',
    )
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
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
        return (f'프로젝트:{self.project_recruitment.project_id}\n'
                f'공고id:{self.project_recruitment_id}'
                f'직무:{self.job_id}\n'
                f'공고상태:{self.recruit_status}\n'
                f'총 인원 제한:{self.total_limit}\n'
                f'현재 참가 성공 인원:{self.current_recruited}')


class ProjectRecruitApplication(models.Model):
    project_recruitment_job = models.ForeignKey(
        ProjectRecruitmentJob,
        on_delete=models.DO_NOTHING,
        help_text='프로젝트 모집 직무',
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING,
        help_text='신청 멤버',
    )
    request_message = models.TextField(
        help_text='신청 메시지',
    )
    request_status = models.CharField(
        max_length=100,
        default=ProjectRecruitApplicationStatus.IN_REVIEW.value,
        choices=ProjectRecruitApplicationStatus.choices(),
        help_text='신청 상태',
    )
    request_status_updated_at = models.DateTimeField(
        help_text='신청 상태 수정 일시',
        null=True,
        blank=True,
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
        return (f'공고id:{self.project_recruitment_job.project_recruitment_id}'
                f'공고직무:{self.project_recruitment_job.job_id}\n'
                f'멤버:{self.member_id}\n'
                f'공고상태:{self.request_status}')


class ProjectMemberManagement(models.Model):
    project_recruit_application = models.ForeignKey(
        ProjectRecruitApplication,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        help_text='프로젝트지원서',
    )
    job = models.ForeignKey(
        'job.Job',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        help_text='프로젝트에서 맡고 있는 직무',
    )
    left_status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=ProjectMemberManagementLeftStatus.choices(),
        help_text='프로젝트 탈퇴 상태',
    )
    is_leader = models.BooleanField(
        default=False,
        help_text='리더 여부',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='생성 일시',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='수정 일시',
    )
    left_status_updated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='프로젝트 탈퇴 상태 수정 일시',
    )

    def __str__(self):
        return (f'프로젝트:{self.project_recruit_application.project_recruitment_job.project_recruitment.project_id}\n'
                f'직무:{self.job_id}\n'
                f'탈주상태:{self.left_status}\n'
                f'리더여부:{self.is_leader}')


class ProjectMemberAttributeReferralReward(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.DO_NOTHING,
        help_text='프로젝트',
    )
    given_member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING,
        help_text='발송인',
        related_name='given_members',
    )
    received_member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING,
        help_text='수취인',
        related_name='received_members',
    )
    member_attribute_type = models.ForeignKey(
        'member.MemberAttributeType',
        on_delete=models.DO_NOTHING,
        help_text='멤버 속성 타입',
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
        return (f'프로젝트:{self.project_id}\n'
                f'발송인:{self.given_member_id}\n'
                f'수취인:{self.received_member_id}\n'
                f'멤버 속성 타입:{self.member_attribute_type_id}')


class ProjectBookmark(models.Model):
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
    is_deleted = models.BooleanField(
        default=False,
        help_text='삭제 여부',
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='삭제 일시',
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
        return (f'프로젝트:{self.project_id}\n'
                f'멤버:{self.member_id}')
