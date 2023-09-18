from django.http import HttpRequest
from django.test import TestCase

from common_decorators.request_decorators import mandatories
from common_exceptions.exceptions import (
    CodeInvalidateException,
    MissingMandatoryParameterException,
)


@mandatories('param1', 'param2')
def my_view_function(request, m):
    return m


class MyViewClass:
    @mandatories('param1', 'param2')
    def my_method(self, request, m):
        return m


class TestMandatoriesDecorator(TestCase):

    def test_decorator_applied_to_function(self):
        # Given: Create a request
        request = HttpRequest()
        request.method = 'GET'
        request.GET = {'param1': 'value1', 'param2': 'value2'}

        # When: Call the decorated function with mandatory parameters
        response = my_view_function(request)

        # Then: Ensure the function executes and returns the expected result
        self.assertEqual(response, {'param1': 'value1', 'param2': 'value2'})

        # When: Call the decorated function with missing mandatory parameter
        request.GET = {'param1': 'value1'}
        with self.assertRaises(MissingMandatoryParameterException):
            my_view_function(request)

    def test_decorator_applied_to_class_method(self):
        # Given: Create a request
        request = HttpRequest()
        request.method = 'GET'
        request.GET = {'param1': 'value1', 'param2': 'value2'}

        # When: Instantiate the class and call the decorated method with mandatory parameters
        view_instance = MyViewClass()
        response = view_instance.my_method(request)

        # Then: Ensure the method executes and returns the expected result
        self.assertEqual(response, {'param1': 'value1', 'param2': 'value2'})

        # When: Instantiate the class and call the decorated method with missing mandatory parameter
        request.GET = {'param1': 'value1'}
        with self.assertRaises(MissingMandatoryParameterException):
            view_instance.my_method(request)

    def test_decorator_without_request_argument(self):
        # When: Call the decorator without a request argument (should raise CodeInvalidateException)
        @mandatories('param1', 'param2')
        def invalid_function():
            pass

        with self.assertRaises(CodeInvalidateException):
            invalid_function()

        class InvalidViewClass:
            @mandatories('param1', 'param2')
            def method(self):
                pass
        # When: Apply the decorator to a class without request arguments (should raise CodeInvalidateException)
        with self.assertRaises(CodeInvalidateException):
            InvalidViewClass().method()
