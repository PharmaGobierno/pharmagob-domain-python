from datetime import datetime, time as day_time, timedelta
from time import time
from typing import Dict, Iterator, List, Optional, Tuple
from zoneinfo import ZoneInfo

from pharmagob.v1.models.inventory_count_schedule import (
    Frequency,
    InventoryCountScheduleModel,
    ScheduleStatus,
)
from pharmagob.v1.repository_interfaces.inventory_count_schedules import (
    InventoryCountScheduleRepositoryInterface,
)

from ._base import UmuScopedService


class InventoryCountScheduleService(
    UmuScopedService[
        InventoryCountScheduleModel, InventoryCountScheduleRepositoryInterface
    ]
):
    __model__ = InventoryCountScheduleModel

    def claim(
        self,
        entity_id: str,
        *,
        expected_statuses: List[ScheduleStatus],
        data: dict,
        umu_id: str,
    ) -> Optional[InventoryCountScheduleModel]:
        result = self.repository.claim(
            entity_id,
            expected_statuses=expected_statuses,
            data={**data, "updated_at": round(time() * 1000)},
            umu_id=umu_id,
        )
        if not result:
            return None
        return InventoryCountScheduleModel(**result)

    def search_by_schedule_name(
        self,
        search_str: str,
        *,
        umu_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        status: Optional[str] = None,
        frequency: Optional[str] = None,
    ) -> Tuple[int, Iterator[InventoryCountScheduleModel]]:
        count, result = self.repository.search_by_schedule_name(
            search_str,
            umu_id=umu_id,
            status=status,
            frequency=frequency,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: InventoryCountScheduleModel(**r), result)

    @staticmethod
    def calculate_next_run_at(
        schedule: InventoryCountScheduleModel, *, after: int, time_zone: str
    ) -> Optional[int]:
        """First occurrence strictly after `after` (epoch ms), or None when it
        falls after `ends_at`.

        Args:
            time_zone: IANA name read by the caller from its environment
                (e.g. "America/Mexico_City"); it is never stored in the model.
        """
        tz = ZoneInfo(time_zone)
        hour, minute = map(int, schedule.run_time.split(":"))
        start = max(after + 1, schedule.starts_at)
        day = datetime.fromtimestamp(start / 1000, tz).date()
        frequency = Frequency(schedule.frequency)

        # MONTHLY day_of_month is 1-28, so a match is always within 62 days
        for _ in range(62):
            if (
                frequency == Frequency.DAILY
                or (frequency == Frequency.WEEKLY and day.isoweekday() == schedule.day_of_week)
                or (frequency == Frequency.MONTHLY and day.day == schedule.day_of_month)
            ):
                run_at = datetime.combine(day, day_time(hour, minute), tzinfo=tz)
                next_run_at = round(run_at.timestamp() * 1000)
                if next_run_at >= start:
                    if schedule.ends_at is not None and next_run_at > schedule.ends_at:
                        return None
                    return next_run_at
            day += timedelta(days=1)
        raise ValueError(f"Invalid schedule definition: {schedule._id}")
