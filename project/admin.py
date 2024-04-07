from django.contrib import admin
from project.models import Project, ProjectManagementPermission


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'current_recruit_status',
        'total_recruitment_time',
        'project_status',
        'project_result_status',
        'job_experience_type',
        'engagement_level',
        'resource_status',
        'project_start_time',
        'project_end_time',
    ]


class ProjectManagementPermissionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'project',
        'member',
        'permission',
        'status',
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectManagementPermission, ProjectManagementPermissionAdmin)
