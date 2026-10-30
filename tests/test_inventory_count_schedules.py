from datetime import datetime
from zoneinfo import ZoneInfo

from pharmagob.v1.models.inventory_count_schedule import (
    Frequency,
    InventoryCountScheduleModel,
)
from pharmagob.v1.models.inventory_count_task import CountScope
from pharmagob.v1.services.inventory_count_schedules import (
    InventoryCountScheduleService,
)

TIME_ZONE = "America/Mexico_City"
TZ = ZoneInfo(TIME_ZONE)
USER = {"id": "planeador@test", "umu_id": "UMU1", "display_name": "Planeador"}


def ms(*args) -> int:
    return round(datetime(*args, tzinfo=TZ).timestamp() * 1000)


def schedule(**kwargs) -> InventoryCountScheduleModel:
    data = {
        "umu_id": "UMU1",
        "schedule_name": "Controlados",
        "frequency": Frequency.DAILY,
        "run_time": "08:00",
        "starts_at": ms(2026, 1, 1),
        "count_scope": CountScope.GENERAL,
        "item_filter": {"families": ["CONTROLLED"]},
        "next_run_at": 0,
        "author": USER,
        "last_author": USER,
    }
    data.update(kwargs)
    return InventoryCountScheduleModel(**data)


def next_run_at(entity, after):
    return InventoryCountScheduleService.calculate_next_run_at(
        entity, after=after, time_zone=TIME_ZONE
    )


def test_daily_same_day_before_run_time():
    assert next_run_at(schedule(), ms(2026, 3, 10, 7, 0)) == ms(2026, 3, 10, 8, 0)


def test_daily_is_strictly_after():
    assert next_run_at(schedule(), ms(2026, 3, 10, 8, 0)) == ms(2026, 3, 11, 8, 0)


def test_not_before_starts_at():
    entity = schedule(starts_at=ms(2026, 6, 1))
    assert next_run_at(entity, ms(2026, 3, 10)) == ms(2026, 6, 1, 8, 0)


def test_weekly_uses_iso_weekday():
    entity = schedule(frequency=Frequency.WEEKLY, day_of_week=1)  # monday
    # 2026-03-11 is a wednesday
    assert next_run_at(entity, ms(2026, 3, 11, 9, 0)) == ms(2026, 3, 16, 8, 0)


def test_monthly_day_28_in_february():
    entity = schedule(frequency=Frequency.MONTHLY, day_of_month=28)
    assert next_run_at(entity, ms(2026, 1, 28, 9, 0)) == ms(2026, 2, 28, 8, 0)


def test_after_ends_at_returns_none():
    entity = schedule(ends_at=ms(2026, 3, 10, 23, 59))
    assert next_run_at(entity, ms(2026, 3, 10, 9, 0)) is None
