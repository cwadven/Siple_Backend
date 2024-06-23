from django.contrib import admin
from job.models import (
    Job,
    JobCategory,
)


class JobCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'display_name',
        'name',
        'is_deleted',
        'is_hidden',
    ]


class JobAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'category',
        'display_name',
        'name',
        'is_deleted',
        'is_hidden',
    ]


admin.site.register(Job, JobAdmin)
admin.site.register(JobCategory, JobCategoryAdmin)
