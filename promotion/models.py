from django.db import models


class PromotionRule(models.Model):
    description = models.TextField(verbose_name='Rule of Detail Description')
    displayable = models.BooleanField(verbose_name='Promotion Displayable', default=False)
    display_start_time = models.DateTimeField(verbose_name='Display Start', null=True, blank=True, db_index=True)
    display_end_time = models.DateTimeField(verbose_name='Display End', null=True, blank=True, db_index=True)
    action_page = models.CharField(
        verbose_name='Action Page',
        max_length=100,
        choices=[
            ('_blank', 'New Page'),
            ('_self', 'Same Page'),
        ],
        null=True,
    )
    target_url = models.TextField(
        verbose_name='Action for using url',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PromotionTag(models.Model):
    name = models.CharField(
        verbose_name='Promotion Tag Name',
        max_length=100,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Banner(models.Model):
    promotion_rule = models.ForeignKey(PromotionRule, on_delete=models.CASCADE)

    title = models.CharField(
        verbose_name='Banner title',
        max_length=100,
        null=True,
        blank=True
    )
    title_font_color = models.CharField(
        verbose_name='Banner title font color',
        max_length=100,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Banner description',
        null=True,
        blank=True,
    )
    description_font_color = models.CharField(
        verbose_name='Banner description font color',
        max_length=100,
        null=True,
        blank=True,
    )
    background_color = models.CharField(
        verbose_name='Banner background color',
        max_length=100,
        null=True,
        blank=True,
    )
    big_image = models.TextField(
        verbose_name='Banner big page for image',
        blank=True,
        null=True,
    )
    middle_image = models.TextField(
        verbose_name='Banner middle page for image',
        blank=True,
        null=True,
    )
    small_image = models.TextField(
        verbose_name='Banner small page for image',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(PromotionTag, blank=True)

    def __str__(self):
        return self.title
