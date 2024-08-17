from common.common_forms.admin_forms import PreSignedUrlAdminForm
from django import forms
from project.models import (
    Project,
    ProjectCategory,
)


class ProjectCategoryAdminForm(PreSignedUrlAdminForm):
    main_image_file = forms.ImageField(
        label='아이콘 이미지 업로드 하기',
        help_text='이미지를 업로드 후, 저장하면 URL이 자동으로 입력됩니다.',
        required=False,
    )

    class Meta:
        model = ProjectCategory
        fields = '__all__'
        target_field_by_image_field = {
            'main_image_file': 'icon_image'
        }
        upload_image_type = 'category_icon_image'


class ProjectAdminForm(PreSignedUrlAdminForm):
    main_image_file = forms.ImageField(
        label='메인 이미지 업로드 하기',
        help_text='이미지를 업로드 후, 저장하면 URL이 자동으로 입력됩니다.',
        required=False,
    )

    class Meta:
        model = Project
        fields = '__all__'
        target_field_by_image_field = {
            'main_image_file': 'main_image'
        }
        upload_image_type = 'project_main_image'
