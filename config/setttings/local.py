from .base import * # noqa


SECRET_KEY = 'development_secret_key'
KAKAO_API_KEY = 'development_KAKAO_API_KEY'
KAKAO_SECRET_KEY = 'development_KAKAO_SECRET_KEY'
NAVER_API_KEY = 'development_NAVER_API_KEY'
NAVER_SECRET_KEY = 'development_NAVER_SECRET_KEY'
GOOGLE_CLIENT_ID = 'development_GOOGLE_CLIENT_ID'
GOOGLE_SECRET_KEY = 'development_GOOGLE_SECRET_KEY'
GOOGLE_REDIRECT_URL = 'development_GOOGLE_REDIRECT_URL'

AWS_IAM_ACCESS_KEY = 'development_AWS_IAM_ACCESS_KEY'
AWS_IAM_SECRET_ACCESS_KEY = 'development_AWS_IAM_SECRET_ACCESS_KEY'
AWS_S3_BUCKET_NAME = 'bucket_name'

EMAIL_HOST_USER = 'development_EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'development_EMAIL_HOST_PASSWORD'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # noqa
    }
}

# CELERY SETTINGS
timezone = 'Asia/Seoul'
CELERY_BROKER_URL = 'redis://localhost:6379/1'
result_backend = 'redis://localhost:6379/1'
accept_content = ["json"]
task_serializer = "json"
result_serializer = "json"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
