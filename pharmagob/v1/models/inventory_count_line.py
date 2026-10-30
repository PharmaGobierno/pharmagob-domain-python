from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from ._base import UpdatableModel, uuid_by_params
from .minified import min_models


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


@dataclass(kw_only=True)
class InventoryCountLineModel(UpdatableModel):
    """One line per location content (item + lot + location) of a task."""

    __entity_name__ = "inventory-count-lines"

    umu_id: str
    task: min_models.CountTaskMin
    item: min_models.ItemMin
    lot: str
    expiration_date: int
    location: min_models.LocationMin
    location_content_id: str  # LocationContentModel _id: uuid_by_params(item.id, lot, location.id)
    is_in_system: bool
    kardex_initial_quantity: int
    counts: List[min_models.CountEntryMin] = field(default_factory=list)
    status: LineStatus = LineStatus.PENDING
    rule: Optional[min_models.CountRuleMin] = None
    resolution: Optional[min_models.CountResolutionMin] = None
    is_open: bool = True  # lock between open tasks of the same count_type (D-02)
    deleted_at: Optional[int] = None  # soft delete, physically purged later (D-09)
    context: Optional[dict] = None
    last_author: min_models.UserMin

    @classmethod
    def _dict_to_dataclasses(cls, instance):
        super()._dict_to_dataclasses(instance)
        instance.counts = [
            min_models.CountEntryMin(**count) if isinstance(count, dict) else count
            for count in instance.counts
        ]
        if isinstance(instance.rule, dict):
            instance.rule = min_models.CountRuleMin(**instance.rule)
        if isinstance(instance.resolution, dict):
            instance.resolution = min_models.CountResolutionMin(**instance.resolution)

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.task.id, self.location_content_id)

    def minified(self) -> min_models.CountLineMin:
        return min_models.CountLineMin(
            id=self._id,
            item_id=self.item.id,
            lot=self.lot,
            location_id=self.location.id,
            status=self.status,
        )
