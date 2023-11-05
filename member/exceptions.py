from common.common_exceptions import ResponseException


class LoginFailedException(ResponseException):
    status_code = 400
    default_detail = '로그인에 실패했습니다.'
    default_code = 'login-error'


class SocialLoginTokenErrorException(ResponseException):
    status_code = 400
    default_detail = '소셜 로그인에 발급된 토큰에 문제가 있습니다.'
    default_code = 'social-token-error'


class BlackMemberException(ResponseException):
    status_code = 400
    default_detail = '정지된 유저입니다.'
    default_code = 'inaccessible-member-login'


class DormantMemberException(ResponseException):
    status_code = 400
    default_detail = '휴면상태의 유저입니다.'
    default_code = 'dormant-member-login'


class LeaveMemberException(ResponseException):
    status_code = 400
    default_detail = '탈퇴상태의 유저입니다.'
    default_code = 'leave-member-login'


class UnknownPlatformException(ResponseException):
    status_code = 400
    default_detail = '알 수 없는 로그인 방식입니다.'
    default_code = 'platform-error'
