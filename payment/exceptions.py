from rest_framework.exceptions import APIException


class UnavailablePayHandler(APIException):
    status_code = 400
    default_detail = '해당 결제로 구매할 수 없는 상품입니다.'
    default_code = 'cannot-buy-with-specific-payment'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }
