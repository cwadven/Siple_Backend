from django.db import models


class JobCategory(models.Model):
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
    is_hidden = models.BooleanField(
        default=False,
        help_text='숨김 여부',
        verbose_name='숨김 여부',
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

    class Meta:
        verbose_name = '직군 카테고리'
        verbose_name_plural = '직군 카테고리'


class Job(models.Model):
    category = models.ForeignKey(
        JobCategory,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name='jobs',
        help_text='직군 카테고리',
        verbose_name='직군 카테고리',
    )
    display_name = models.CharField(max_length=256)
    name = models.CharField(max_length=256, db_index=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.display_name} - {self.name}'

    class Meta:
        verbose_name = '직업'
        verbose_name_plural = '직업'
