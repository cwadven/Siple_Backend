from django.contrib import admin
from job.models import Job


class JobAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'display_name',
        'name',
        'is_deleted',
        'is_hidden',
    ]


admin.site.register(Job, JobAdmin)
