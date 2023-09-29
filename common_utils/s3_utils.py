import boto3
import uuid
from botocore.config import Config
from botocore.exceptions import ClientError

from django.conf import settings


def generate_presigned_url(file_name, _type='common', unique=0, expires_in=1000):
    s3_client = boto3.client(
        's3',
        region_name='ap-northeast-2',
        aws_access_key_id=settings.AWS_IAM_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_IAM_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )
    try:
        response = s3_client.generate_presigned_post(
            Bucket=settings.AWS_S3_BUCKET_NAME,
            Key=f'{_type}/{unique}/{uuid.uuid4()}_{file_name}',
            Conditions=[
                ['content-length-range', 0, 10485760]
            ],
            ExpiresIn=expires_in
        )
        return response
    except ClientError as e:
        raise Exception(e)
