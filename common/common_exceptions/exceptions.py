from collections import defaultdict
from typing import (
    Dict,
    List,
    Optional,
)

from rest_framework.exceptions import (
    APIException,
    _get_error_details,
)


class ResponseException(APIException):
    status_code = 400
    default_detail = '예상치 못한 에러가 발생했습니다.'
    default_code = 'unexpected-error'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }


class CommonAPIException(APIException):
    status_code = 500
    default_detail = '예상치 못한 에러가 발생했습니다.'
    default_code = 'unexpected-error'

    def __init__(self, status_code: int, error_summary: str, error_code: str, errors: Dict[str, List[str]] = None):
        self.status_code = status_code
        self.default_detail = error_summary
        self.default_code = error_code
        self.errors = errors


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


class PydanticAPIException(CommonAPIException):
    def __init__(self, status_code: int, error_summary: str = None, error_code: str = None, errors: List[dict] = None):
        """
        'errors' parameter Structure is different from CommonAPIException
        """
        self.status_code = status_code
        self.default_detail = error_summary
        self.default_code = error_code
        self.errors = self.format_errors(errors)
        self.detail = _get_error_details(error_summary, error_code)

    @staticmethod
    def format_errors(errors: Optional[List[dict]]):
        formatted_errors = defaultdict(list)
        if not errors:
            return None
        for error in errors:
            field = error['loc'][0]
            message = error['msg'].split(',', 1)[-1].strip()
            formatted_errors[field].append(message)
        return formatted_errors
