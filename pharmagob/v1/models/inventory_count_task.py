from enum import Enum


class CountType(str, Enum):
    PHYSICAL = "PHYSICAL"
    CYCLIC = "CYCLIC"


class CyclicMode(str, Enum):
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"


class CountScope(str, Enum):
    ALL = "ALL"
    GENERAL = "GENERAL"  # location label_code STANDARD
    BIENESTAR = "BIENESTAR"  # location label_code FARB


class TaskStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    RELEASING = "RELEASING"
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
