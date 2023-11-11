from django.contrib import admin

from member.models import (
    Member,
    MemberProvider,
    MemberStatus,
    MemberType,
)


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


admin.site.register(Member, MemberAdmin)
admin.site.register(MemberProvider, MemberProviderAdmin)
admin.site.register(MemberStatus, MemberStatusAdmin)
admin.site.register(MemberType, MemberTypeAdmin)
