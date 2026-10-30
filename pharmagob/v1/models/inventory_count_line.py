from enum import Enum


class LineStatus(str, Enum):
    PENDING = "PENDING"
    SECOND_COUNT = "SECOND_COUNT"
    VALIDATION = "VALIDATION"
    ADJUSTMENT = "ADJUSTMENT"
    APPLYING = "APPLYING"
    CLOSED = "CLOSED"
    ADJUSTED = "ADJUSTED"
    REJECTED = "REJECTED"


class LineResolution(str, Enum):
    NO_DIFFERENCE = "NO_DIFFERENCE"
    ADJUSTED = "ADJUSTED"
    REJECTED = "REJECTED"


class ResolutionOrigin(str, Enum):
    RULES = "RULES"
    AUDIT = "AUDIT"
    ADJUSTMENTS = "ADJUSTMENTS"
