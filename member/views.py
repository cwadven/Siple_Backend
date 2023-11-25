from django.contrib.auth import (
    authenticate,
    login,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from common.common_decorators.request_decorators import mandatories
from common.common_utils import get_jwt_login_token
from member.dtos.request_dtos import NormalLoginRequest, SocialLoginRequest
from member.dtos.response_dtos import NormalLoginResponse, SocialLoginResponse
from member.models import Member


class LoginView(APIView):
    @mandatories('username', 'password')
    def post(self, request, m):
        normal_login_request = NormalLoginRequest(
            username=m['username'],
            password=m['password'],
        )
        member = authenticate(
            request,
            username=normal_login_request.username,
            password=normal_login_request.password
        )
        if not member:
            return Response({'message': '아이디 및 비밀번호 정보가 일치하지 않습니다.'}, status=400)

        login(request, member)
        normal_login_response = NormalLoginResponse(access_token=get_jwt_login_token(member))
        return Response(normal_login_response.model_dump(), status=200)


class SocialLoginView(APIView):
    @mandatories('provider', 'token')
    def post(self, request, m):
        social_login_request = SocialLoginRequest(
            token=m['token'],
            provider=m['provider'],
        )
        member, is_created = Member.objects.get_or_create_member_by_token(
            social_login_request.token,
            social_login_request.provider,
        )
        member.raise_if_inaccessible()

        login(request, member)
        social_login_response = SocialLoginResponse(
            access_token=get_jwt_login_token(member),
            is_created=is_created,
        )
        return Response(social_login_response.model_dump(), status=200)
