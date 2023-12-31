from rest_framework.exceptions import APIException


class OrderNotExists(APIException):
    status_code = 400
    default_detail = '존재하지 않는 주문입니다.'
    default_code = 'order-not-exists'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }
