from rest_framework_jwt.settings import api_settings

from member.models import Member


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_jwt_login_token(member: Member) -> str:
    payload = jwt_payload_handler(member)
    token = jwt_encode_handler(payload)
    return token
