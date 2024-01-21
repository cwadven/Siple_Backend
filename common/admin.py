from django.contrib import admin
from common.models import (
    BlackListWord,
    BlackListSection,
)


class BlackListSectionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]


class BlackListWordAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'wording',
        'black_list_section',
    ]


admin.site.register(BlackListSection, BlackListSectionAdmin)
admin.site.register(BlackListWord, BlackListWordAdmin)
