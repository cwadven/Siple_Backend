from django.db import models

from member.models import Guest


class GuestPoint(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.DO_NOTHING)
    point = models.BigIntegerField(db_index=True)
    reason = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Guest 포인트'
        verbose_name_plural = 'Guest 포인트'

    def __str__(self):
        return f'{self.guest} - {self.point} - is_active: {self.is_active}'
