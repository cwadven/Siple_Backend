from django.contrib import admin
from member.models import (
    Guest,
    Member,
    MemberInformation,
    MemberJobExperience,
    MemberProvider,
    MemberStatus,
    MemberType,
)


class GuestAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'ip',
        'temp_nickname',
        'email',
        'member',
        'is_blacklisted',
        'last_joined_at',
    ]


class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nickname',
        'member_type',
        'member_status',
        'member_provider',
    ]


class MemberProviderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description'
    ]


class MemberStatusAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description'
    ]


class MemberTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description'
    ]


class MemberJobExperienceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'member',
        'job',
        'start_date',
        'end_date',
        'is_deleted',
    ]


class MemberInformationAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'member',
        'description',
        'is_deleted',
    ]


admin.site.register(Guest, GuestAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberProvider, MemberProviderAdmin)
admin.site.register(MemberStatus, MemberStatusAdmin)
admin.site.register(MemberType, MemberTypeAdmin)
admin.site.register(MemberJobExperience, MemberJobExperienceAdmin)
admin.site.register(MemberInformation, MemberInformationAdmin)
