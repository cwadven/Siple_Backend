from unittest.mock import patch

from common.common_testcase_helpers.job.testcase_helpers import create_job_category_for_testcase
from common.exceptions import InvalidPathParameterException
from django.test import TestCase
from django.urls import reverse
from member.models import Member
from rest_framework.test import APITestCase


class HealthCheckViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('common:health_check')

    def test_health_check_when_success(self):
        # Given:
        # When:
        response = self.client.get(self.url)

        # Then:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'OK'})


class ConstanceTypeViewTest(TestCase):
    def test_constance_type_should_raise_error_when_invalid_key_for_mapper(self):
        # Given:
        invalid_key = 'invalid_key'

        # When:
        response = self.client.get(
            reverse('common:constance_type', kwargs={'constance_type': invalid_key})
        )

        # Then:
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message': InvalidPathParameterException.default_detail,
                'error_code': InvalidPathParameterException.default_code,
                'errors': None,
            },
        )

    def test_constance_type_should_return_job_category_helper(self):
        # Given:
        constance_type = 'job-category'
        # And:
        web_category1 = create_job_category_for_testcase('web_category1')
        web_category2 = create_job_category_for_testcase('web_category2')

        # When:
        response = self.client.get(
            reverse('common:constance_type', kwargs={'constance_type': constance_type})
        )

        # Then: response should be success
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            {data['id'] for data in response.json()['data']},
            {web_category1.id, web_category2.id},
        )
        self.assertEqual(
            {data['display_name'] for data in response.json()['data']},
            {web_category1.display_name, web_category2.display_name},
        )
        self.assertEqual(
            {data['name'] for data in response.json()['data']},
            {web_category1.name, web_category2.name},
        )


class ConstanceJobTypeViewTest(TestCase):
    @patch('common.helpers.constance_helpers.ConstanceJobDetailTypeHelper.get_constance_detail_types')
    def test_constance_job_type_should_return_job_detail_type_helper(self, mock_get_constance_detail_types):
        # Given:
        mock_get_constance_detail_types.return_value = []

        # When:
        response = self.client.get(reverse('common:constance_job_type'))

        # Then:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data': []})
        # And:
        mock_get_constance_detail_types.assert_called_once()


class ConstanceProjectCategoryTypeViewTest(TestCase):
    @patch('common.helpers.constance_helpers.ConstanceProjectCategoryIconImageTypeHelper.get_constance_icon_image_types')
    def test_constance_job_type_should_return_job_detail_type_helper(self, mock_get_constance_icon_image_types):
        # Given:
        mock_get_constance_icon_image_types.return_value = []

        # When:
        response = self.client.get(reverse('common:constance_project_category_type'))

        # Then:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'data': []})
        # And:
        mock_get_constance_icon_image_types.assert_called_once()


class GetPreSignedURLViewTest(APITestCase):
    def setUp(self):
        self.member = Member.objects.create_user(username='test1', nickname='test1')

    def test_get_pre_signed_url_should_return_401_when_not_login(self):
        # Given:
        constance_type = 'project-image'
        transaction_pk = 'transaction_pk'
        # And:
        data = {
            'file_name': 'file_name',
        }

        # When:
        response = self.client.post(
            reverse(
                'common:get_pre_signed_url',
                kwargs={
                    'constance_type': constance_type,
                    'transaction_pk': transaction_pk,
                },
            ),
            data,
        )

        # Then:
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            {
                'message': '로그인이 필요합니다.',
                'error_code': 'login-required',
                'errors': None,
            }
        )

    def test_get_pre_signed_url_should_return_400_when_invalid_query_params(self):
        # Given: Login
        self.client.force_login(self.member)
        # And:
        constance_type = 'project-image'
        transaction_pk = 'transaction_pk'
        # And:
        data = {
            'invalid_key': 'invalid_value',
        }

        # When:
        response = self.client.post(
            reverse(
                'common:get_pre_signed_url',
                kwargs={
                    'constance_type': constance_type,
                    'transaction_pk': transaction_pk,
                },
            ),
            data,
        )

        # Then:
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message': '입력값을 다시 한번 확인해주세요.',
                'error_code': '400-pre_signed_url_input_data-00001',
                'errors': {'file_name': ['문자열 형식으로 입력해주세요.']},
            },
        )

    def test_get_pre_signed_url_should_return_400_when_invalid_constance_type(self):
        # Given: Login
        self.client.force_login(self.member)
        # And:
        constance_type = 'invalid_key'
        transaction_pk = 'transaction_pk'
        # And:
        data = {
            'file_name': 'file_name',
        }

        # When:
        response = self.client.post(
            reverse(
                'common:get_pre_signed_url',
                kwargs={
                    'constance_type': constance_type,
                    'transaction_pk': transaction_pk,
                },
            ),
            data,
        )

        # Then:
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'message': InvalidPathParameterException.default_detail,
                'error_code': InvalidPathParameterException.default_code,
                'errors': None,
            },
        )

    @patch('common.views.generate_pre_signed_url_info')
    def test_get_pre_signed_url_should_return_500_when_external_api_exception_raise(self,
                                                                                    mock_generate_pre_signed_url_info):
        # Given: Login
        self.client.force_login(self.member)
        # And:
        constance_type = 'project-image'
        transaction_pk = 'transaction_pk'
        # And:
        data = {
            'file_name': 'file_name',
        }
        # And: mock external api exception
        mock_generate_pre_signed_url_info.side_effect = Exception('raise')

        # When:
        response = self.client.post(
            reverse(
                'common:get_pre_signed_url',
                kwargs={
                    'constance_type': constance_type,
                    'transaction_pk': transaction_pk,
                },
            ),
            data,
        )

        # Then:
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(),
            {
                'message': '외부 API 통신 중 에러가 발생했습니다.',
                'error_code': 'external-api-error',
                'errors': None,
            },
        )

    @patch('common.views.generate_pre_signed_url_info')
    def test_get_pre_signed_url_should_return_data_when_success(self,
                                                                mock_generate_pre_signed_url_info):
        # Given: Login
        self.client.force_login(self.member)
        # And:
        constance_type = 'project-image'
        transaction_pk = 'transaction_pk'
        # And:
        data = {
            'file_name': 'file_name',
        }
        # And: mock data
        mock_generate_pre_signed_url_info.return_value = {
            'url': 'url',
            'fields': {'key': 'value'},
        }

        # When:
        response = self.client.post(
            reverse(
                'common:get_pre_signed_url',
                kwargs={
                    'constance_type': constance_type,
                    'transaction_pk': transaction_pk,
                },
            ),
            data,
        )

        # Then:
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'url': 'url',
                'data': {
                    'key': 'value'
                },
            },
        )
