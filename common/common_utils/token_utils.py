from datetime import (
    timedelta,
    datetime,
)

from rest_framework_jwt.compat import (
    get_username,
)
from rest_framework_jwt.settings import api_settings

from member.models import Member


jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def jwt_payload_handler(member: Member):
    username = get_username(member)
    payload = {
        'member_id': member.pk,
        'email': member.email,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'username': username,
    }
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
