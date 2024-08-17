from django.contrib import admin
from project.forms.admin_forms import (
    ProjectAdminForm,
    ProjectCategoryAdminForm,
)
from project.models import (
    Project,
    ProjectBookmark,
    ProjectCategory,
    ProjectManagementPermission,
    ProjectMemberAttributeReferralReward,
    ProjectMemberManagement,
    ProjectRecruitApplication,
    ProjectRecruitment,
    ProjectRecruitmentJob,
)


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'current_recruit_status',
        'total_recruitment_time',
        'project_status',
        'project_result_status',
        'job_experience_type',
        'resource_status',
        'project_start_time',
        'project_end_time',
    ]
    form = ProjectAdminForm


class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'display_name',
        'name',
        'is_deleted',
    ]
    form = ProjectCategoryAdminForm


class ProjectManagementPermissionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project',
        'member',
        'permission',
        'status',
    ]


class ProjectRecruitmentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project',
        'times_project_recruit',
        'recruit_status',
    ]


class ProjectRecruitmentJobAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project_recruitment',
        'job',
        'total_limit',
        'current_recruited',
        'recruit_status',
    ]


class ProjectRecruitApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project_recruitment_job',
        'member',
        'request_status',
    ]


class ProjectMemberManagementAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project_recruit_application',
        'job',
        'left_status',
        'is_leader',
    ]


class ProjectMemberAttributeReferralRewardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project',
        'given_member',
        'received_member',
        'member_attribute_type',
    ]


class ProjectBookmarkAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project',
        'member',
        'is_deleted',
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(ProjectManagementPermission, ProjectManagementPermissionAdmin)
admin.site.register(ProjectRecruitment, ProjectRecruitmentAdmin)
admin.site.register(ProjectRecruitmentJob, ProjectRecruitmentJobAdmin)
admin.site.register(ProjectRecruitApplication, ProjectRecruitApplicationAdmin)
admin.site.register(ProjectMemberManagement, ProjectMemberManagementAdmin)
admin.site.register(ProjectMemberAttributeReferralReward, ProjectMemberAttributeReferralRewardAdmin)
admin.site.register(ProjectBookmark, ProjectBookmarkAdmin)
