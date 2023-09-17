class ResponseException(Exception):
    status_code = 400
    default_detail = '예상치 못한 에러가 발생했습니다.'
    default_code = 'unexpected-error'

    @classmethod
    def to_message(cls):
        return {
            'message': cls.default_detail,
        }
