from abc import (
    ABC,
    abstractmethod,
)


class CursorCriteria(ABC):
    @abstractmethod
    def is_valid_decoded_cursor(self, decoded_cursor: dict):
        pass
