from rest_framework.exceptions import APIException


class NotEnoughGuestPoints(APIException):
    status_code = 400
    default_detail = '포인트가 부족합니다.'
    default_code = 'not-enough-guest-points'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }
