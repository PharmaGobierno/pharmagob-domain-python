from dataclasses import asdict

import pytest

from pharmagob.v1.models.inventory_count_line import LineStatus
from pharmagob.v1.models.minified import min_models
from pharmagob.v1.services.inventory_count_tasks import (
    LINE_STAGE_COUNTERS,
    line_stage_increments,
)

FINAL_STATUSES = {LineStatus.CLOSED, LineStatus.ADJUSTED, LineStatus.REJECTED}


def test_counters_default_to_zero_and_keep_the_existing_ones():
    assert asdict(min_models.CountLinesQuantitiesMin(total_quantity=10)) == {
        "total_quantity": 10,
        "counted_quantity": 0,
        "resolved_quantity": 0,
        "pending_quantity": 0,
        "second_count_quantity": 0,
        "validation_quantity": 0,
        "adjustment_quantity": 0,
    }


def test_a_task_document_without_the_new_counters_still_loads():
    # tasks written before DOM-12 only carry the three original counters
    old = {"total_quantity": 10, "counted_quantity": 4, "resolved_quantity": 1}
    assert min_models.CountLinesQuantitiesMin(**old).pending_quantity == 0


def test_every_open_status_has_a_counter_and_final_statuses_have_none():
    assert set(LineStatus) - set(LINE_STAGE_COUNTERS) == FINAL_STATUSES
    fields = set(min_models.CountLinesQuantitiesMin.__dataclass_fields__)
    assert set(LINE_STAGE_COUNTERS.values()) <= fields


def test_first_count_moves_lines_out_of_pending():
    transitions = [
        (LineStatus.PENDING, LineStatus.SECOND_COUNT),
        (LineStatus.PENDING, LineStatus.SECOND_COUNT),
        (LineStatus.PENDING, LineStatus.CLOSED),
    ]
    assert line_stage_increments(transitions) == {
        "lines.pending_quantity": -3,
        "lines.second_count_quantity": 2,
    }


def test_second_count_splits_between_audit_adjustment_and_closed():
    transitions = [
        (LineStatus.SECOND_COUNT, LineStatus.VALIDATION),
        (LineStatus.SECOND_COUNT, LineStatus.VALIDATION),
        (LineStatus.SECOND_COUNT, LineStatus.ADJUSTMENT),
        (LineStatus.SECOND_COUNT, LineStatus.CLOSED),
    ]
    assert line_stage_increments(transitions) == {
        "lines.second_count_quantity": -4,
        "lines.validation_quantity": 2,
        "lines.adjustment_quantity": 1,
    }


def test_a_new_out_of_system_line_only_adds():
    assert line_stage_increments([(None, LineStatus.SECOND_COUNT)]) == {
        "lines.second_count_quantity": 1
    }


def test_applying_is_counted_as_adjustment():
    assert line_stage_increments([(LineStatus.ADJUSTMENT, LineStatus.APPLYING)]) == {}
    assert line_stage_increments([(LineStatus.APPLYING, LineStatus.ADJUSTED)]) == {
        "lines.adjustment_quantity": -1
    }
    assert line_stage_increments([(LineStatus.APPLYING, LineStatus.VALIDATION)]) == {
        "lines.adjustment_quantity": -1,
        "lines.validation_quantity": 1,
    }


def test_statuses_are_accepted_as_strings_and_empty_batches_add_nothing():
    assert line_stage_increments([("VALIDATION", "REJECTED")]) == {
        "lines.validation_quantity": -1
    }
    assert line_stage_increments([]) == {}


def test_an_unknown_status_is_an_error():
    with pytest.raises(ValueError):
        line_stage_increments([("PENDING", "NOT_A_STATUS")])


def test_a_full_task_keeps_the_invariant():
    """10 lines: 5 counted (3 to second count, 2 closed), then the other 5
    (all to second count), then 3 second counts (2 to audit, 1 to adjustment)."""
    counters = asdict(
        min_models.CountLinesQuantitiesMin(total_quantity=10, pending_quantity=10)
    )

    def apply(transitions, resolved=0, counted=0):
        for key, delta in line_stage_increments(transitions).items():
            counters[key.removeprefix("lines.")] += delta
        counters["resolved_quantity"] += resolved
        counters["counted_quantity"] += counted
        open_lines = sum(counters[name] for name in set(LINE_STAGE_COUNTERS.values()))
        assert open_lines + counters["resolved_quantity"] == counters["total_quantity"]
        assert counters["counted_quantity"] == (
            counters["total_quantity"] - counters["pending_quantity"]
        )

    pending, second, audit, adjustment, closed = (
        LineStatus.PENDING,
        LineStatus.SECOND_COUNT,
        LineStatus.VALIDATION,
        LineStatus.ADJUSTMENT,
        LineStatus.CLOSED,
    )
    apply([(pending, second)] * 3 + [(pending, closed)] * 2, resolved=2, counted=5)
    assert counters["pending_quantity"] == 5
    apply([(pending, second)] * 5, counted=5)
    assert (counters["pending_quantity"], counters["second_count_quantity"]) == (0, 8)
    apply([(second, audit)] * 2 + [(second, adjustment)])
    assert (counters["validation_quantity"], counters["adjustment_quantity"]) == (2, 1)
    apply([(adjustment, LineStatus.APPLYING)])
    apply([(LineStatus.APPLYING, LineStatus.ADJUSTED)], resolved=1)
    assert counters["adjustment_quantity"] == 0
