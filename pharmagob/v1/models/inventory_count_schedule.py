from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import UpdatableModel
from .inventory_count_task import CountScope
from .minified import min_models


class Frequency(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


class ScheduleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CANCELLED = "CANCELLED"


@dataclass(kw_only=True)
class InventoryCountScheduleModel(UpdatableModel):
    """Recurring cyclic count. The time zone used to read run_time and to
    calculate next_run_at is a service environment variable, never a field."""

    __entity_name__ = "inventory-count-schedules"

    umu_id: str
    schedule_name: str
    frequency: Frequency
    run_time: str  # "HH:MM", local time
    day_of_week: Optional[int] = None  # 1-7 (monday = 1), WEEKLY only
    day_of_month: Optional[int] = None  # 1-28, MONTHLY only
    starts_at: int
    ends_at: Optional[int] = None
    count_scope: CountScope
    item_filter: min_models.CountItemFilterMin
    task_validity_days: int = 7
    status: ScheduleStatus = ScheduleStatus.ACTIVE
    next_run_at: int
    last_task: Optional[min_models.CountTaskMin] = None
    last_run_at: Optional[int] = None
    author: min_models.UserMin
    last_author: min_models.UserMin

    @classmethod
    def _dict_to_dataclasses(cls, instance):
        super()._dict_to_dataclasses(instance)
        if isinstance(instance.last_task, dict):
            instance.last_task = min_models.CountTaskMin(**instance.last_task)

    def minified(self) -> min_models.CountScheduleMin:
        return min_models.CountScheduleMin(
            id=self._id,
            schedule_name=self.schedule_name,
            frequency=self.frequency,
        )
