import pytest

from pharmagob.v1.models.inventory_count_event import (
    AuditActivity,
    Events,
    InventoryCountEventModel,
)
from pharmagob.v1.models.inventory_count_task import CountType
from pharmagob.v1.models.minified import min_models

AUTHOR = min_models.UserMin(id="auditor@umu", umu_id="UMU-1", display_name="Auditor")
TASK = min_models.CountTaskMin(
    id="task-1", reference_id="CF-000001", task_name="Anual", count_type="PHYSICAL"
)
LINE = min_models.CountLineMin(
    id="line-1", item_id="010.000.0103.00", lot="L1", location_id="loc-1", status="VALIDATION"
)


def _event(event, *, transition_timestamp=1_000, context=None, task=TASK, schedule=None):
    return InventoryCountEventModel(
        umu_id="UMU-1",
        author=AUTHOR,
        event=event,
        activity=AuditActivity.MODIFICATION,
        count_type=CountType.PHYSICAL,
        task=task,
        line=LINE,
        schedule=schedule,
        context=context or {},
        transition_timestamp=transition_timestamp,
    )


def test_task_and_line_events_ignore_the_clock():
    assert _event(Events.TASK_RELEASED, transition_timestamp=1)._id == _event(
        Events.TASK_RELEASED, transition_timestamp=2
    )._id
    assert _event(Events.ADJUSTMENT_NEGATIVE, transition_timestamp=1)._id == _event(
        Events.ADJUSTMENT_NEGATIVE, transition_timestamp=2
    )._id


def test_event_id_is_stable_when_event_is_read_back_as_str():
    assert _event(Events.REJECTED)._id == _event("REJECTED")._id


def test_audit_validated_repeats_per_validated_round():
    # H-13 / H-15: a second validation after returning to audit is a new event
    first = _event(Events.AUDIT_VALIDATED, transition_timestamp=1_000)
    second = _event(Events.AUDIT_VALIDATED, transition_timestamp=2_000)
    assert first._id != second._id
    # the same counted_at is the same event (publisher re-execution)
    assert first._id == _event(Events.AUDIT_VALIDATED, transition_timestamp=1_000)._id


def test_returned_to_audit_uses_returned_at_from_context():
    context = {"returned_to_audit": {"reason": "INSUFFICIENT_STOCK", "returned_at": 5_000}}
    event = _event(Events.ADJUSTMENT_RETURNED_TO_AUDIT, transition_timestamp=9_999, context=context)
    same = _event(Events.ADJUSTMENT_RETURNED_TO_AUDIT, transition_timestamp=1, context=context)
    other = _event(
        Events.ADJUSTMENT_RETURNED_TO_AUDIT,
        context={"returned_to_audit": {"reason": "SENT_BY_AUDITOR", "returned_at": 6_000}},
    )
    assert event._id == same._id
    assert event._id != other._id


def test_count_captured_discriminates_by_author_and_counted_at():
    other_author = min_models.UserMin(id="contador-2", umu_id="UMU-1", display_name="")
    base = _event(Events.COUNT_CAPTURED, transition_timestamp=1_000)
    assert base._id != _event(Events.COUNT_CAPTURED, transition_timestamp=1_001)._id
    other = InventoryCountEventModel(
        umu_id="UMU-1",
        author=other_author,
        event=Events.COUNT_CAPTURED,
        activity=AuditActivity.MODIFICATION,
        count_type=CountType.PHYSICAL,
        task=TASK,
        transition_timestamp=1_000,
    )
    assert base._id != other._id


def test_schedule_run_skipped_requires_next_run_at():
    schedule = min_models.CountScheduleMin(id="sch-1", schedule_name="Semanal", frequency="WEEKLY")
    with pytest.raises(ValueError):
        _event(Events.SCHEDULE_RUN_SKIPPED, task=None, schedule=schedule)
    skipped = _event(
        Events.SCHEDULE_RUN_SKIPPED, task=None, schedule=schedule, context={"next_run_at": 7_000}
    )
    assert skipped._id == InventoryCountEventModel.generate_event_id(
        Events.SCHEDULE_RUN_SKIPPED, schedule_id="sch-1", next_run_at=7_000
    )


def test_rebuilds_min_models_from_mongo_dicts():
    doc = _event(Events.REJECTED).dict()
    rebuilt = InventoryCountEventModel(**doc)
    assert rebuilt._id == doc["_id"]
    assert isinstance(rebuilt.task, min_models.CountTaskMin)
    assert isinstance(rebuilt.line, min_models.CountLineMin)
