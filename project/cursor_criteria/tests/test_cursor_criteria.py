from datetime import (
    datetime,
)
from unittest.mock import patch

from common.common_testcase_helpers.testcase_helpers import SampleModel
from django.test import TestCase
from project.cursor_criteria.cursor_criteria import HomeProjectListCursorCriteria


class HomeProjectListCursorCriteriaTests(TestCase):
    def test_is_valid_decoded_cursor_valid(self):
        # Given: valid cursor
        cursor = {
            'id__lt': 123,
            'rearrangement_time__lte': '2021-08-01T12:00:00+00:00',
        }
        # Expect: True
        self.assertEqual(
            HomeProjectListCursorCriteria.is_valid_decoded_cursor(cursor),
            True,
        )

    def test_is_valid_decoded_cursor_invalid(self):
        # Given: invalid cursor
        cursor = {
            'id__lt': 123,
        }
        # Expect: False
        self.assertEqual(
            HomeProjectListCursorCriteria.is_valid_decoded_cursor(cursor),
            False,
        )

    @patch('common.common_criteria.cursor_criteria.data_to_urlsafe_base64')
    def test_get_encoded_base64_cursor_data(self, mock_data_to_urlsafe_base64):
        # Given: Mock data_to_urlsafe_base64
        mock_data_to_urlsafe_base64.return_value = 'encoded_string'
        # And: Sample data
        data = SampleModel(
            id=1,
            rearrangement_time=datetime(2021, 8, 1, 12, 0, 1),
        )

        # When: get_encoded_base64_cursor_data
        result = HomeProjectListCursorCriteria.get_encoded_base64_cursor_data(data)

        # Then: expected result
        self.assertEqual(result, 'encoded_string')
        # And: data_to_urlsafe_base64 called with expected dict
        expected_dict = {
            'id__lt': 1,
            'rearrangement_time__lte': '2021-08-01T12:00:01+09:00',  # Assumes date formatting in valid_keys handling
        }
        # And: data_to_urlsafe_base64 called with expected dict
        mock_data_to_urlsafe_base64.assert_called_once_with(expected_dict)

    def test_get_encoded_base64_cursor_data_invalid_key(self):
        # Given: Sample data with missing attribute for cursor_keys 'datestamp'
        data = SampleModel(
            id=1,
            name="Project",
            timestamp=datetime(2021, 8, 1),
        )

        # When: get_encoded_base64_cursor_data
        with self.assertRaises(ValueError) as e:
            HomeProjectListCursorCriteria.get_encoded_base64_cursor_data(data)

        # Then: expected exception
        self.assertEqual(
            e.exception.args[0],
            'Attribute \'rearrangement_time\' not found in \'SampleModel\'',
        )
