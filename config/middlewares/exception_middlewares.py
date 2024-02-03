from config.settings.base import logger
from rest_framework import exceptions
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    logger.error(f'{exc}, {context}')

    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, exceptions.ParseError):
            message = exc.detail
        elif isinstance(exc, exceptions.AuthenticationFailed):
            message = exc.detail
        elif isinstance(exc, exceptions.NotAuthenticated):
            message = 'No Auth'
        elif isinstance(exc, exceptions.PermissionDenied):
            message = exc.detail
        elif isinstance(exc, exceptions.NotFound):
            message = exc.detail
        elif isinstance(exc, exceptions.MethodNotAllowed):
            message = exc.detail
        elif isinstance(exc, exceptions.NotAcceptable):
            message = exc.detail
        elif isinstance(exc, exceptions.UnsupportedMediaType):
            message = exc.detail
        elif isinstance(exc, exceptions.Throttled):
            message = exc.detail
        elif isinstance(exc, exceptions.ValidationError):
            message = exc.detail
        elif isinstance(exc, exceptions.APIException):
            message = exc.detail

        response.data['message'] = message

        try:
            del response.data['detail']
        except KeyError:
            pass

        return response
    else:
        return response
