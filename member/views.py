from django.contrib.auth import login

from rest_framework.views import APIView
from rest_framework.response import Response

from common_decorators.request_decorators import mandatories
from common_utils.token_utils import get_jwt_login_token
from member.models import Member


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
