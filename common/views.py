import boto3
from botocore.config import Config
from common.common_consts.common_error_messages import InvalidInputResponseErrorStatus
from common.common_exceptions import PydanticAPIException
from common.common_utils import generate_pre_signed_url_info
from common.consts import IMAGE_CONSTANCE_TYPES
from common.dtos.request_dtos import GetPreSignedURLRequest
from common.dtos.response_dtos import (
    ConstanceDetailTypeResponse,
    ConstanceIconImageTypeResponse,
    ConstanceTypeResponse,
    GetPreSignedURLResponse,
    HealthCheckResponse,
)
from common.exceptions import (
    ExternalAPIException,
    InvalidPathParameterException,
)
from common.helpers.constance_helpers import (
    CONSTANCE_TYPE_HELPER_MAPPER,
    ConstanceJobDetailTypeHelper,
    ConstanceProjectCategoryIconImageTypeHelper,
)
from django.conf import settings
from member.permissions import IsMemberLogin
from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request):
        return Response(HealthCheckResponse(message='OK').model_dump(), status=200)


class ConstanceJobTypeView(APIView):
    def get(self, request):
        constance_job_detail_type_helper = ConstanceJobDetailTypeHelper()
        return Response(
            ConstanceDetailTypeResponse(data=constance_job_detail_type_helper.get_constance_detail_types()).model_dump(),
            status=200,
        )


class ConstanceProjectCategoryTypeView(APIView):
    def get(self, request):
        constance_project_category_detail_type_helper = ConstanceProjectCategoryIconImageTypeHelper()
        return Response(
            ConstanceIconImageTypeResponse(
                data=constance_project_category_detail_type_helper.get_constance_icon_image_types()
            ).model_dump(),
            status=200,
        )


class ConstanceTypeView(APIView):
    def get(self, request, constance_type: str):
        constance_type_helper = CONSTANCE_TYPE_HELPER_MAPPER.get(constance_type)
        if not constance_type_helper:
            raise InvalidPathParameterException()
        return Response(
            ConstanceTypeResponse(data=constance_type_helper.get_constance_types()).model_dump(),
            status=200,
        )


class GetPreSignedURLView(APIView):
    permission_classes = [
        IsMemberLogin,
    ]

    def post(self, request, constance_type: str, transaction_pk: str):
        try:
            pre_signed_url_request = GetPreSignedURLRequest.of(request.data)
        except ValidationError as e:
            raise PydanticAPIException(
                status_code=400,
                error_summary=InvalidInputResponseErrorStatus.INVALID_PRE_SIGNED_URL_INPUT_DATA_400.label,
                error_code=InvalidInputResponseErrorStatus.INVALID_PRE_SIGNED_URL_INPUT_DATA_400.value,
                errors=e.errors(),
            )

        if constance_type not in IMAGE_CONSTANCE_TYPES:
            raise InvalidPathParameterException()

        try:
            s3_client = boto3.client(
                's3',
                region_name='ap-northeast-2',
                aws_access_key_id=settings.AWS_IAM_ACCESS_KEY,
                aws_secret_access_key=settings.AWS_IAM_SECRET_ACCESS_KEY,
                config=Config(signature_version='s3v4')
            )
            info = generate_pre_signed_url_info(
                s3_client,
                settings.AWS_S3_BUCKET_NAME,
                pre_signed_url_request.file_name,
                constance_type,
                transaction_pk,
                same_file_name=True,
            )
            url = info['url']
            data = info['fields']
        except Exception:
            raise ExternalAPIException()

        return Response(
            GetPreSignedURLResponse(
                url=url,
                data=data,
            ).model_dump(),
            status=200,
        )
