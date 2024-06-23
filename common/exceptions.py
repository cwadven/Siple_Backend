from common.common_exceptions import CommonAPIException


class InvalidPathParameterException(CommonAPIException):
    status_code = 400
    default_detail = '입력값을 다시 확인해주세요.'
    default_code = 'invalid-path-parameter'
