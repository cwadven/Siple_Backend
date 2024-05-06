from datetime import (
    date,
    datetime,
)
from typing import Any

from common.common_interfaces.cursor_criteria_interfaces import CursorCriteriaInterface
from common.common_utils.encode_utils import data_to_urlsafe_base64


class CursorCriteria(CursorCriteriaInterface):
    cursor_keys = []

    @classmethod
    def is_valid_decoded_cursor(cls, decoded_cursor: dict) -> bool:
        for cursor_key in cls.cursor_keys:
            if decoded_cursor.get(cursor_key) is None:
                return False
        return True

    @classmethod
    def get_encoded_base64_cursor_data(cls, data: Any) -> str:
        encoding_data = {}

        for cursor_key in cls.cursor_keys:
            attribute = cursor_key.split('__')[0]
            try:
                value = getattr(data, attribute)
            except AttributeError:
                raise ValueError(f"Attribute '{attribute}' not found in '{data.__class__.__name__}'")
            if isinstance(value, (datetime, date)):
                encoding_data[cursor_key] = value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                encoding_data[cursor_key] = value

        return data_to_urlsafe_base64(encoding_data)
