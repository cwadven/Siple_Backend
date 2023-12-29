from django.contrib import admin

from member.models import (
    Guest,
    Member,
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


admin.site.register(Guest, GuestAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberProvider, MemberProviderAdmin)
admin.site.register(MemberStatus, MemberStatusAdmin)
admin.site.register(MemberType, MemberTypeAdmin)
