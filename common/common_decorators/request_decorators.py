from functools import wraps
from types import FunctionType

from common.common_exceptions.exceptions import (
    CodeInvalidateException,
    MissingMandatoryParameterException,
)
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest
from rest_framework.exceptions import APIException
from rest_framework.request import Request


def mandatories(*keys):
    def _mandatories(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Here we assume that the first argument is the request
            request = next((x for x in args if isinstance(x, (WSGIRequest, HttpRequest, Request))), None)
            if request is None:
                raise CodeInvalidateException()
            mandatory = dict()
            for key in keys:
                try:
                    if request.method == 'GET':
                        data = request.GET[key]
                    else:
                        data = request.POST[key]
                    if data in ['', None]:
                        raise MissingMandatoryParameterException()
                except KeyError:
                    try:
                        json_body = request.data
                        data = json_body[key]
                        if data in ['', None]:
                            raise MissingMandatoryParameterException()
                    except Exception:
                        raise MissingMandatoryParameterException()
                mandatory[key] = data
            return func(m=mandatory, *args, **kwargs)
        return wrapper

    def decorator(cls_or_func):
        if isinstance(cls_or_func, FunctionType):
            return _mandatories(cls_or_func)
        else:
            for attr_name, attr_value in cls_or_func.__dict__.items():
                if callable(attr_value):
                    setattr(cls_or_func, attr_name, _mandatories(attr_value))
            return cls_or_func

    return decorator


def optionals(*keys):
    def _optionals(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Here we assume that the first argument is the request
            request = next((x for x in args if isinstance(x, (WSGIRequest, HttpRequest, Request))), None)
            if request is None:
                raise CodeInvalidateException()
            optional = dict()
            for arg in keys:
                for key, val in arg.items():
                    try:
                        if request.method == 'GET':
                            data = request.GET[key]
                        else:
                            data = request.POST[key]
                        if data is None:
                            data = val
                    except KeyError:
                        try:
                            json_body = request.data
                            data = json_body[key]
                            if data is None:
                                data = val
                        except Exception:
                            data = val
                    optional[key] = data
            return func(o=optional, *args, **kwargs)
        return wrapper

    def decorator(cls_or_func):
        if isinstance(cls_or_func, FunctionType):
            return _optionals(cls_or_func)
        else:
            for attr_name, attr_value in cls_or_func.__dict__.items():
                if callable(attr_value):
                    setattr(cls_or_func, attr_name, _optionals(attr_value))
            return cls_or_func

    return decorator


def pagination(default_size=10):
    def _paging(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Here we assume that the first argument is the request
            request = next((x for x in args if isinstance(x, (WSGIRequest, HttpRequest, Request))), None)
            if request is None:
                raise CodeInvalidateException()
            try:
                page = int(request.GET.get('page', 1)) - 1
                size = int(request.GET.get('size', default_size))
                start_row = page * size
                end_row = (page + 1) * size
            except APIException as e:
                raise APIException(e)
            return func(start_row=start_row, end_row=end_row, *args, **kwargs)
        return wrapper

    def decorator(cls_or_func):
        if isinstance(cls_or_func, FunctionType):
            return _paging(cls_or_func)
        else:
            for attr_name, attr_value in cls_or_func.__dict__.items():
                if callable(attr_value):
                    setattr(cls_or_func, attr_name, _paging(attr_value))
            return cls_or_func

    return decorator
