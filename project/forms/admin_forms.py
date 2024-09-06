import boto3
from botocore.config import Config
from common.common_forms.admin_forms import PreSignedUrlAdminForm
from django import forms
from django.conf import settings
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
        boto_client = boto3.client(
            's3',
            region_name='ap-northeast-2',
            aws_access_key_id=settings.AWS_IAM_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_IAM_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4')
        )
        upload_bucket_name = settings.AWS_S3_BUCKET_NAME
        cloud_front_domain = settings.AWS_CLOUD_FRONT_DOMAIN


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
        boto_client = boto3.client(
            's3',
            region_name='ap-northeast-2',
            aws_access_key_id=settings.AWS_IAM_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_IAM_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4')
        )
        upload_bucket_name = settings.AWS_S3_BUCKET_NAME
        cloud_front_domain = settings.AWS_CLOUD_FRONT_DOMAIN
