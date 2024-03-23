from django.db import models


class Job(models.Model):
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
