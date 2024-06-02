from common.common_exceptions import (
    CommonAPIException,
)


class LoginFailedException(CommonAPIException):
    status_code = 400
    default_detail = '로그인에 실패했습니다.'
    default_code = 'login-error'


class NormalLoginFailedException(CommonAPIException):
    status_code = 400
    default_detail = '아이디 및 비밀번호 정보가 일치하지 않습니다.'
    default_code = 'invalid-username-or-password'


class SocialLoginTokenErrorException(CommonAPIException):
    status_code = 400
    default_detail = '소셜 로그인에 발급된 토큰에 문제가 있습니다.'
    default_code = 'social-token-error'


class InvalidRefreshTokenErrorException(CommonAPIException):
    status_code = 401
    default_detail = '잘못된 리프레시 토큰입니다.'
    default_code = 'invalid-refresh-token'


class InvalidValueForSignUpFieldErrorException(CommonAPIException):
    status_code = 400
    default_detail = '입력값을 다시 확인해주세요.'
    default_code = 'invalid-sign-up-field-value'


class BlackMemberException(CommonAPIException):
    status_code = 400
    default_detail = '정지된 유저입니다.'
    default_code = 'inaccessible-member-login'


class DormantMemberException(CommonAPIException):
    status_code = 400
    default_detail = '휴면상태의 유저입니다.'
    default_code = 'dormant-member-login'


class LeaveMemberException(CommonAPIException):
    status_code = 400
    default_detail = '탈퇴상태의 유저입니다.'
    default_code = 'leave-member-login'


class UnknownPlatformException(CommonAPIException):
    status_code = 400
    default_detail = '알 수 없는 로그인 방식입니다.'
    default_code = 'platform-error'
