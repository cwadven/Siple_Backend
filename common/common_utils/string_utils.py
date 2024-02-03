import random
import string
from typing import (
    List,
    Sequence,
    Union,
)


def generate_random_string_digits(length: int = 4) -> str:
    return ''.join(random.choice(string.digits) for _ in range(length))


def get_filtered_by_startswith_text_and_convert_to_standards(startswith_text: str, keys: Sequence, is_integer=False) -> List[Union[str, int]]:
    """
    Filters keys that start with a specific text from an iterable type,
    and converts the values of specific portions of the keys to integers based on the provided condition.

    [ Example ]
    If startswith_text is 'home_popup_modal_':
    Input: ['home_popup_modal_1', 'home_popup_modal_2', 'home_popup_modal_3', 'home_popup_modal_4', 'k_popup_modal_10']
    Output (if is_integer=True): [1, 2, 3, 4]
    Output (if is_integer=False): ['1', '2', '3', '4']

    :param startswith_text: The text that the keys should start with for filtering.
    :param keys: An iterable containing keys to be filtered and processed.
    :param is_integer: Determines whether the extracted values should be converted to integers.
    :return: A list containing filtered and processed values based on the specified conditions.
    """
    return [
        int(key.replace(startswith_text, '')) if is_integer else key.replace(startswith_text, '')
        for key in keys if key.startswith(startswith_text)
    ]
