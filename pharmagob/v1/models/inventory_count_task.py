from enum import Enum


class CountType(str, Enum):
    PHYSICAL = "PHYSICAL"
    CYCLIC = "CYCLIC"


class CyclicMode(str, Enum):
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"


FARB_LABEL_CODE = "FARB"  # location label_code of Farmacias del Bienestar


class CountScope(str, Enum):
    ALL = "ALL"
    GENERAL = "GENERAL"  # location label_code NOT IN ["FARB"] (H-17)
    BIENESTAR = "BIENESTAR"  # location label_code FARB

    def to_location_filter(self) -> dict:
        """Location filters for LocationContentRepositoryInterface
        (`get_batch_after`, `search_by_item`), so every service translates
        the scope the same way. GENERAL is `label_code NOT IN ["FARB"]`:
        location contents without label_code count as general, the same
        rule the inventory API applies (H-17). Never use `== "STANDARD"`."""
        if self is CountScope.GENERAL:
            return {
                "location_label_code": None,
                "location_label_code_not_in": [FARB_LABEL_CODE],
            }
        if self is CountScope.BIENESTAR:
            return {
                "location_label_code": FARB_LABEL_CODE,
                "location_label_code_not_in": None,
            }
        return {"location_label_code": None, "location_label_code_not_in": None}


class TaskStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    RELEASING = "RELEASING"
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
