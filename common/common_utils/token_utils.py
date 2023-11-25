import uuid
from datetime import (
    timedelta,
    datetime,
)

from calendar import timegm
from rest_framework_jwt.compat import (
    get_username_field,
    get_username,
)
from rest_framework_jwt.settings import api_settings

from member.models import Member


jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def jwt_payload_handler(member: Member):
    username_field = get_username_field()
    username = get_username(member)

    payload = {
        'member_id': member.pk,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if hasattr(member, 'email'):
        payload['email'] = member.email
    if isinstance(member.pk, uuid.UUID):
        payload['member_id'] = str(member.pk)

    payload[username_field] = username

    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def get_jwt_login_token(member: Member) -> str:
    payload = jwt_payload_handler(member)
    token = jwt_encode_handler(payload)
    return token


def get_jwt_refresh_token(member: Member) -> str:
    refresh_expiration = timedelta(days=7)
    refresh_token = jwt_encode_handler({
        'member_id': member.id,
        'exp': datetime.utcnow() + refresh_expiration
    })
    return refresh_token
