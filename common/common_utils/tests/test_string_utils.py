from datetime import (
    date,
    datetime,
    timedelta,
    timezone,
)
from unittest.mock import patch

from common.common_utils.string_utils import (
    format_iso8601,
    generate_random_string_digits,
    get_filtered_by_startswith_text_and_convert_to_standards,
)
from django.test import TestCase


@patch("common.common_utils.string_utils.random.choice")
class TestStringUtils(TestCase):
    def test_generate_random_string_digits_default_length(self, mock_choice):
        # Given: Mocking random
        mock_choice.return_value = "1"

        # When:
        result = generate_random_string_digits()

        # Then:
        self.assertEqual(len(result), 4)
        self.assertEqual(result, "1111")

    def test_generate_random_string_digits_custom_length(self, mock_choice):
        # Given: Mocking random
        mock_choice.return_value = "1"
        length = 6

        # When:
        result = generate_random_string_digits(length)

        # Then:
        self.assertEqual(len(result), length)
        self.assertEqual(result, "111111")

    def test_generate_random_string_digits_zero_length(self, mock_choice):
        # Given: Mocking random
        mock_choice.return_value = "1"

        # When:
        result = generate_random_string_digits(0)

        # Then:
        self.assertEqual(result, '')


class TestFilteredConversion(TestCase):
    def test_get_filtered_by_startswith_text_with_is_integer_true(self):
        # Given:
        input_keys = ['home_popup_modal_1', 'home_popup_modal_2', 'home_popup_modal_3', 'home_popup_modal_4', 'k_popup_modal_10']

        # When: is_integer with True
        result = get_filtered_by_startswith_text_and_convert_to_standards('home_popup_modal_', input_keys, is_integer=True)

        # Then:
        self.assertEqual(result, [1, 2, 3, 4])

    def test_get_filtered_by_startswith_text_with_is_integer_false(self):
        # Given:
        input_keys = ['home_popup_modal_1', 'home_popup_modal_2', 'home_popup_modal_3', 'home_popup_modal_4', 'k_popup_modal_10']

        # When: is_integer with False
        result = get_filtered_by_startswith_text_and_convert_to_standards('home_popup_modal_', input_keys, is_integer=False)

        # Then:
        self.assertEqual(result, ['1', '2', '3', '4'])


class FormatISO8601Tests(TestCase):

    def test_format_datetime(self):
        # Given: A datetime object
        dt = datetime(2024, 5, 1, 13, 0, 0, tzinfo=timezone.utc)

        # When: The datetime object is formatted
        result = format_iso8601(dt)

        # Then: The datetime object is formatted correctly
        self.assertEqual(result, "2024-05-01T13:00:00+00:00")

    def test_format_date(self):
        # Given: A date object
        d = date(2024, 5, 1)

        # When: The date object is formatted
        result = format_iso8601(d)

        # Then: The date object is formatted correctly
        self.assertEqual(result, "2024-05-01T00:00:00+09:00")

    def test_format_date_with_date_timezone(self):
        # Given: A date object
        d = date(2024, 5, 1)

        # When: The date object is formatted
        result = format_iso8601(d, date_timezone='+02:00')

        # Then: The date object is formatted correctly
        self.assertEqual(result, "2024-05-01T00:00:00+02:00")

    def test_invalid_type(self):
        # Given: An object of an unsupported type
        d = 'invalid_type'

        # Expected: A TypeError is raised
        with self.assertRaises(TypeError):
            format_iso8601(d)

    def test_datetime_with_timezone_offset(self):
        # Given: A datetime object with a timezone offset
        dt = datetime(2024, 5, 1, 13, 0, 0, tzinfo=timezone(timedelta(hours=2)))

        # When: The datetime object is formatted
        result = format_iso8601(dt)

        # Then: The datetime object is formatted correctly
        self.assertEqual(result, "2024-05-01T13:00:00+02:00")

    def test_datetime_without_timezone_offset(self):
        # Given: A datetime object with a timezone offset
        dt = datetime(2024, 5, 1, 13, 0, 0)

        # When: The datetime object is formatted
        result = format_iso8601(dt)

        # Then: The datetime object is formatted correctly
        self.assertEqual(result, "2024-05-01T13:00:00+09:00")

    def test_datetime_with_microseconds(self):
        # Given: A datetime object with microseconds
        dt = datetime(2024, 5, 1, 13, 0, 0, 500000, tzinfo=timezone.utc)

        # When: The datetime object is formatted
        result = format_iso8601(dt)

        # Then: The datetime object is formatted correctly
        self.assertEqual(result, "2024-05-01T13:00:00+00:00")
