from django.contrib.auth.models import AbstractUser
from django.db import models

from member.consts import MemberStatusExceptionTypeSelector
from member.managers import MemberManager


class MemberProvider(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class MemberStatus(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class MemberType(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Member(AbstractUser):
    nickname = models.CharField(max_length=45, blank=True, null=True, db_index=True, unique=True)
    member_type = models.ForeignKey(MemberType, models.DO_NOTHING, blank=True, null=True)
    member_status = models.ForeignKey(MemberStatus, models.DO_NOTHING, blank=True, null=True)
    member_provider = models.ForeignKey(MemberProvider, models.DO_NOTHING, blank=True, null=True)
    profile_image_url = models.CharField(max_length=256, blank=True, null=True)

    objects = MemberManager()

    class Meta:
        verbose_name = '일반 사용자'
        verbose_name_plural = '일반 사용자'

    def raise_if_inaccessible(self):
        if self.member_status_id != 1:
            raise MemberStatusExceptionTypeSelector(self.member_status_id).selector()
