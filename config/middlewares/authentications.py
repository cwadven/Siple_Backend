import jwt
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication, get_authorization_header
from rest_framework_jwt.settings import api_settings


jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class DefaultAuthentication(SessionAuthentication):
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)

        if jwt_value is None:
            member = getattr(request._request, 'user', None)
            if not member:
                return None, None
            member.raise_if_inaccessible()
            self.enforce_csrf(request)
            return member, None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('만료된 토큰입니다.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('잘못된 토큰 형식입니다.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = _('유효하지 않은 토큰 입니다.')
            raise exceptions.AuthenticationFailed(msg)

        member = self.authenticate_credentials(payload)
        member.raise_if_inaccessible()
        return member, jwt_value

    def enforce_csrf(self, request):
        return

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        if smart_str(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_header(self, request):
        return '{0} realm="{1}"'.format(api_settings.JWT_AUTH_HEADER_PREFIX, self.www_authenticate_realm)

    def authenticate_credentials(self, payload):
        Member = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('잘못된 Token 입니다.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            member = Member.objects.get_by_natural_key(username)
        except Member.DoesNotExist:
            msg = _('존재하지 않는 유저입니다.')
            raise exceptions.AuthenticationFailed(msg)

        return member
