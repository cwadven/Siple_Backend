from rest_framework.exceptions import APIException


class ResponseException(Exception):
    status_code = 400
    default_detail = '예상치 못한 에러가 발생했습니다.'
    default_code = 'unexpected-error'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }


class MissingMandatoryParameterException(APIException):
    status_code = 400
    default_detail = '입력값을 다시 확인해주세요.'
    default_code = 'missing-mandatory-parameter'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }


class CodeInvalidateException(APIException):
    status_code = 400
    default_detail = '서버에 문제가 있습니다.'
    default_code = 'invalidate-exception'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }
