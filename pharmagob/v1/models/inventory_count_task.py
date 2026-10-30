from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ._base import UpdatableModel
from .minified import min_models


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


@dataclass(kw_only=True)
class InventoryCountTaskModel(UpdatableModel):
    __entity_name__ = "inventory-count-tasks"

    umu_id: str
    reference_id: str  # e.g. CF-000001, assigned from reference-counters
    task_name: str
    count_type: CountType
    cyclic_mode: Optional[CyclicMode] = None
    count_scope: CountScope
    item_filter: Optional[min_models.CountItemFilterMin] = None
    is_zero_stock_included: bool = False
    scheduled_at: int
    released_at: Optional[int] = None
    expires_at: Optional[int] = None
    status: TaskStatus = TaskStatus.SCHEDULED
    schedule: Optional[min_models.CountScheduleMin] = None
    lines: min_models.CountLinesQuantitiesMin = field(
        default_factory=min_models.CountLinesQuantitiesMin
    )
    author: min_models.UserMin
    last_author: min_models.UserMin

    @classmethod
    def _dict_to_dataclasses(cls, instance):
        super()._dict_to_dataclasses(instance)
        if isinstance(instance.item_filter, dict):
            instance.item_filter = min_models.CountItemFilterMin(**instance.item_filter)
        if isinstance(instance.schedule, dict):
            instance.schedule = min_models.CountScheduleMin(**instance.schedule)

    def minified(self) -> min_models.CountTaskMin:
        return min_models.CountTaskMin(
            id=self._id,
            reference_id=self.reference_id,
            task_name=self.task_name,
            count_type=self.count_type,
        )
