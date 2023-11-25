from django.contrib.auth import (
    authenticate,
    login,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from common.common_decorators.request_decorators import mandatories
from common.common_utils import get_jwt_login_token
from member.models import Member


class LoginView(APIView):
    @mandatories('username', 'password')
    def post(self, request, m):
        member = authenticate(request, username=m['username'], password=m['password'])
        if not member:
            return Response({'message': '아이디 및 비밀번호 정보가 일치하지 않습니다.'}, status=400)

        login(request, member)
        context = {
            'access_token': get_jwt_login_token(member),
        }
        return Response(context, status=200)


class SocialLoginView(APIView):
    @mandatories('provider', 'token')
    def post(self, request, m):
        member, is_created = Member.objects.get_or_create_member_by_token(m['token'], m['provider'])
        member.raise_if_inaccessible()

        login(request, member)

        context = {
            'access_token': get_jwt_login_token(member),
            'is_created': is_created,
        }

        return Response(context, status=200)
