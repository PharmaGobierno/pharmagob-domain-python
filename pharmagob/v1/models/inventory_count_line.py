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


class ReturnToAuditReason(str, Enum):
    """`context.returned_to_audit.reason` of a line sent back to VALIDATION."""

    INSUFFICIENT_STOCK = "INSUFFICIENT_STOCK"  # conditional $inc found no document (H-13)
    SENT_BY_AUDITOR = "SENT_BY_AUDITOR"  # movements since the count, auditor decides (H-15)
