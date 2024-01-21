import jwt
from django.contrib.auth import (
    authenticate,
)
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from common.common_decorators.request_decorators import mandatories
from common.common_utils import (
    generate_random_string_digits,
    get_jwt_guest_token,
    get_jwt_login_token,
    get_jwt_refresh_token,
    get_request_ip,
)
from common.common_utils.cache_utils import (
    generate_dict_value_by_key_to_cache,
    get_cache_value_by_key,
    increase_cache_int_value_by_key,
    delete_cache_value_by_key,
)
from config.middlewares.authentications import jwt_decode_handler
from member.dtos.request_dtos import (
    NormalLoginRequest,
    RefreshTokenRequest,
    SocialLoginRequest,
    SignUpEmailTokenSendRequest,
    SignUpEmailTokenValidationEndRequest,
    SignUpValidationRequest,
)
from member.dtos.response_dtos import (
    NormalLoginResponse,
    RefreshTokenResponse,
    SocialLoginResponse, GuestTokenGetOrCreateResponse,
)
from member.models import Member, Guest
from member.consts import (
    MemberCreationExceptionMessage,
    MemberProviderEnum,
    MemberTypeEnum,
    SIGNUP_EMAIL_TOKEN_TTL,
    SIGNUP_MACRO_COUNT,
    SIGNUP_MACRO_VALIDATION_KEY,
)
from member.services import (
    check_email_exists,
    check_nickname_exists,
    check_username_exists,
)

from .tasks import send_one_time_token_email
from .validators.sign_up_validators import SignUpPayloadValidator


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

        normal_login_response = NormalLoginResponse(
            access_token=get_jwt_login_token(member),
            refresh_token=get_jwt_refresh_token(member.guest),
        )
        return Response(normal_login_response.model_dump(), status=200)


class SocialLoginView(APIView):
    @mandatories('provider', 'token')
    @transaction.atomic
    def post(self, request, m):
        social_login_request = SocialLoginRequest(
            token=m['token'],
            provider=m['provider'],
        )
        member, is_created = Member.objects.get_or_create_member_by_token(
            social_login_request.token,
            social_login_request.provider,
        )
        if is_created:
            if not request.guest:
                request.guest = Guest(ip=get_request_ip(request))
            request.guest.temp_nickname = member.nickname
            request.guest.email = member.email
            request.guest.member = member
            request.guest.save()

        member.raise_if_inaccessible()

        social_login_response = SocialLoginResponse(
            access_token=get_jwt_login_token(member),
            refresh_token=get_jwt_refresh_token(member.guest),
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
                refresh_token=get_jwt_refresh_token(member.guest),
            )
        except (Member.DoesNotExist, jwt.InvalidTokenError):
            return Response({'message': '잘못된 리프레시 토큰입니다.'}, status=401)
        return Response(refresh_token_response.model_dump(), status=200)


class SignUpEmailTokenSendView(APIView):
    @mandatories('email', 'username', 'nickname', 'password2')
    def post(self, request, m):
        sign_up_email_token_send_request = SignUpEmailTokenSendRequest(
            email=m['email'],
            username=m['username'],
            nickname=m['nickname'],
            password2=m['password2'],
        )
        generate_dict_value_by_key_to_cache(
            key=sign_up_email_token_send_request.email,
            value={
                'one_time_token': generate_random_string_digits(),
                'email': sign_up_email_token_send_request.email,
                'username': sign_up_email_token_send_request.username,
                'nickname': sign_up_email_token_send_request.nickname,
                'password2': sign_up_email_token_send_request.password2,
            },
            expire_seconds=SIGNUP_EMAIL_TOKEN_TTL
        )
        value = get_cache_value_by_key(sign_up_email_token_send_request.email)
        if value:
            send_one_time_token_email.apply_async(
                (
                    sign_up_email_token_send_request.email,
                    value['one_time_token'],
                )
            )
            return Response({'message': '인증번호를 이메일로 전송했습니다.'}, 200)
        return Response({'message': '인증번호를 이메일로 전송하지 못했습니다.'}, 400)


class SignUpEmailTokenValidationEndView(APIView):
    @mandatories('email', 'one_time_token')
    @transaction.atomic
    def post(self, request, m):
        payload = SignUpEmailTokenValidationEndRequest(
            email=m['email'],
            one_time_token=m['one_time_token']
        )
        macro_count = increase_cache_int_value_by_key(
            key=SIGNUP_MACRO_VALIDATION_KEY.format(payload.email),
        )
        if macro_count >= SIGNUP_MACRO_COUNT:
            return Response(
                data={
                    'message': '{}회 이상 인증번호를 틀리셨습니다. 현 이메일은 {}시간 동안 인증할 수 없습니다.'.format(
                        SIGNUP_MACRO_COUNT,
                        24
                    )
                },
                status=400,
            )

        value = get_cache_value_by_key(payload.email)

        if not value:
            return Response({'message': '이메일 인증번호를 다시 요청하세요.'}, 400)

        if not value.get('one_time_token') or value.get('one_time_token') != payload.one_time_token:
            return Response({'message': '인증번호가 다릅니다.'}, 400)

        if check_username_exists(value['username']):
            return Response({'message': MemberCreationExceptionMessage.USERNAME_EXISTS.label}, 400)
        if check_nickname_exists(value['nickname']):
            return Response({'message': MemberCreationExceptionMessage.NICKNAME_EXISTS.label}, 400)
        if check_email_exists(value['email']):
            return Response({'message': MemberCreationExceptionMessage.EMAIL_EXISTS.label}, 400)

        member = Member.objects.create_user(
            username=value['username'],
            nickname=value['nickname'],
            email=value['email'],
            member_type_id=MemberTypeEnum.NORMAL_MEMBER.value,
            password=value['password2'],
            member_provider_id=MemberProviderEnum.EMAIL.value,
        )
        if not request.guest:
            request.guest = Guest(ip=get_request_ip(request))
        request.guest.temp_nickname = member.nickname
        request.guest.email = member.email
        request.guest.member = member
        request.guest.save()

        delete_cache_value_by_key(value['email'])
        delete_cache_value_by_key(SIGNUP_MACRO_VALIDATION_KEY.format(payload.email))
        return Response({'message': '회원가입에 성공했습니다.'}, 200)


class SignUpValidationView(APIView):
    @mandatories('username', 'email', 'nickname', 'password1', 'password2')
    def post(self, request, m):
        payload = SignUpValidationRequest(
            username=m['username'],
            nickname=m['nickname'],
            email=m['email'],
            password1=m['password1'],
            password2=m['password2'],
        )
        payload_validator = SignUpPayloadValidator(payload.model_dump())
        error_dict = payload_validator.validate()
        if error_dict:
            return Response(error_dict, 400)
        return Response({'message': 'success'}, 200)


class GetOrCreateGuestTokenView(APIView):
    def post(self, request):
        ip = get_request_ip(request)
        guest = Guest.objects.filter(
            ip=ip,
            member__isnull=True,
        ).last()
        if not guest:
            guest = Guest.objects.create(
                ip=ip,
                temp_nickname=f'비회원{generate_random_string_digits(8)}'
            )
        guest_token_get_or_create_response = GuestTokenGetOrCreateResponse(
            access_token=get_jwt_guest_token(guest),
            refresh_token=get_jwt_refresh_token(guest),
        )
        return Response(guest_token_get_or_create_response.model_dump(), status=200)
