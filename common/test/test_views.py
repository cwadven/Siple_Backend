from unittest.mock import patch

from common.common_testcase_helpers.job.testcase_helpers import create_job_category_for_testcase
from common.exceptions import InvalidPathParameterException
from django.test import TestCase
from django.urls import reverse


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
