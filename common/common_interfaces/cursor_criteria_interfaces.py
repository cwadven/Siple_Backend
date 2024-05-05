from abc import (
    ABC,
    abstractmethod,
)


class CursorCriteria(ABC):
    @classmethod
    @abstractmethod
    def is_valid_decoded_cursor(cls, decoded_cursor: dict) -> bool:
        """Define this method to validate decoded cursors in subclasses."""
        pass
