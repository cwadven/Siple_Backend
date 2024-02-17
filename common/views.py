from common.dtos.response_dtos import HealthCheckResponse
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    def get(self, request):
        return Response(HealthCheckResponse(message='OK').model_dump(), status=200)
