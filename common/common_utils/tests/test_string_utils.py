from unittest.mock import patch

from django.test import TestCase

from common.common_utils.string_utils import (
    generate_random_string_digits,
    get_filtered_by_startswith_text_and_convert_to_standards,
)


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
