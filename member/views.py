import jwt
from django.contrib.auth import (
    authenticate,
    login,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from common.common_decorators.request_decorators import mandatories
from common.common_utils import (
    generate_random_string_digits,
    get_jwt_login_token,
    get_jwt_refresh_token,
)
from common.common_utils.cache_utils import generate_dict_value_by_key_to_cache, get_cache_value_by_key
from config.middlewares.authentications import jwt_decode_handler
from member.dtos.request_dtos import (
    NormalLoginRequest,
    RefreshTokenRequest,
    SocialLoginRequest,
)
from member.dtos.response_dtos import (
    NormalLoginResponse,
    RefreshTokenResponse,
    SocialLoginResponse,
)
from member.models import Member
from .consts import SIGNUP_EMAIL_TOKEN_TTL

from .tasks import send_one_time_token_email


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
        normal_login_response = NormalLoginResponse(
            access_token=get_jwt_login_token(member),
            refresh_token=get_jwt_refresh_token(member),
        )
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
            refresh_token=get_jwt_refresh_token(member),
            is_created=is_created,
        )
        return Response(social_login_response.model_dump(), status=200)


class RefreshTokenView(APIView):
    @mandatories('refresh_token')
    def post(self, request, m):
        refresh_token_request = RefreshTokenRequest(
            refresh_token=m['refresh_token'],
        )
        try:
            payload = jwt_decode_handler(refresh_token_request.refresh_token)
            member = Member.objects.get(id=payload.get('member_id'))
            refresh_token_response = RefreshTokenResponse(
                access_token=get_jwt_login_token(member),
                refresh_token=get_jwt_refresh_token(member),
            )
        except (Member.DoesNotExist, jwt.InvalidTokenError):
            return Response({'message': '잘못된 리프레시 토큰입니다.'}, status=401)
        return Response(refresh_token_response.model_dump(), status=200)


class SignUpEmailTokenSendView(APIView):
    @mandatories('email', 'username', 'nickname', 'password2')
    def post(self, request, m):
        generate_dict_value_by_key_to_cache(
            key=m['email'],
            value={
                'one_time_token': generate_random_string_digits(),
                'email': m['email'],
                'username': m['username'],
                'nickname': m['nickname'],
                'password2': m['password2'],
            },
            expire_seconds=SIGNUP_EMAIL_TOKEN_TTL
        )
        value = get_cache_value_by_key(m['email'])
        if value:
            send_one_time_token_email.apply_async(
                (
                    m['email'],
                    value['one_time_token'],
                )
            )
            return Response({'message': '인증번호를 이메일로 전송했습니다.'}, 200)
        return Response({'message': '인증번호를 이메일로 전송하지 못했습니다.'}, 400)


# class SignUpValidationView(APIView):
#     @mandatories('username', 'email', 'nickname', 'password1', 'password2')
#     def post(self, request, m):
#         payload_validator = SignUpPayloadValidator(m)
#         try:
#             payload_validator.validate()
#         except ValidationError as e:
#             return Response(e.detail, 400)
#         return Response({'result': 'success'}, 200)
#
#
# class SignUpEmailTokenValidationEndView(APIView):
#     @mandatories('email', 'one_time_token')
#     def post(self, request, m):
#         macro_count = increase_cache_int_value_by_key(
#             key=SIGNUP_MACRO_VALIDATION_KEY.format(m['email']),
#         )
#         if macro_count >= SIGNUP_MACRO_COUNT:
#             return Response(
#                 data={
#                     'message': '{}회 이상 인증번호를 틀리셨습니다. 현 이메일은 {}시간 동안 인증할 수 없습니다.'.format(
#                         SIGNUP_MACRO_COUNT,
#                         24
#                     )
#                 },
#                 status=400,
#             )
#
#         value = get_cache_value_by_key(m['email'])
#
#         if not value:
#             return Response({'message': '이메일 인증번호를 다시 요청하세요.'}, 400)
#
#         if not value.get('one_time_token') or value.get('one_time_token') != m['one_time_token']:
#             return Response({'message': '인증번호가 다릅니다.'}, 400)
#
#         # 회원 가입 제약을 위해 더블 체킹 validation
#         if is_username_exists(value['username']):
#             return Response({'message': UserCreationExceptionMessage.USERNAME_EXISTS.label}, 400)
#         if is_nickname_exists(value['nickname']):
#             return Response({'message': UserCreationExceptionMessage.NICKNAME_EXISTS.label}, 400)
#         if is_email_exists(value['email']):
#             return Response({'message': UserCreationExceptionMessage.EMAIL_EXISTS.label}, 400)
#
#         User.objects.create_user(
#             username=value['username'],
#             nickname=value['nickname'],
#             email=value['email'],
#             user_type_id=UserTypeEnum.NORMAL_USER.value,
#             password=value['password2'],
#             user_provider_id=UserProviderEnum.EMAIL.value,
#         )
#
#         # 캐시 서버 기록 삭제 (메크로 및 정보 보존용)
#         delete_cache_value_by_key(value['email'])
#         delete_cache_value_by_key(SIGNUP_MACRO_VALIDATION_KEY.format(m['email']))
#         return Response({'message': '회원가입에 성공했습니다.'}, 200)
