from abc import (
    ABC,
    abstractmethod,
)
from typing import Any


class CursorCriteria(ABC):
    @classmethod
    @abstractmethod
    def is_valid_decoded_cursor(cls, decoded_cursor: dict) -> bool:
        """Define this method to validate decoded cursors in subclasses."""
        pass

    def get_encoded_base64_cursor_data(self, data: Any) -> str:
        """Define this method to get cursor data in subclasses."""
        pass
