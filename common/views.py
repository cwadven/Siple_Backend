from common.dtos.response_dtos import (
    ConstanceDetailTypeResponse,
    ConstanceTypeResponse,
    HealthCheckResponse,
)
from common.exceptions import InvalidPathParameterException
from common.helpers.constance_helpers import (
    CONSTANCE_TYPE_HELPER_MAPPER,
    ConstanceJobDetailTypeHelper,
)
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


class ConstanceTypeView(APIView):
    def get(self, request, constance_type: str):
        constance_type_helper = CONSTANCE_TYPE_HELPER_MAPPER.get(constance_type)
        if not constance_type_helper:
            raise InvalidPathParameterException()
        return Response(
            ConstanceTypeResponse(data=constance_type_helper.get_constance_types()).model_dump(),
            status=200,
        )
