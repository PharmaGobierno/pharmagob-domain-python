from dataclasses import asdict

import pytest

from pharmagob.v1.models.inventory_count_line import LineStatus
from pharmagob.v1.models.minified import min_models
from pharmagob.v1.services.inventory_count_tasks import (
    LINE_DONE_COUNTERS,
    LINE_REJECTED_COUNTERS,
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
        "second_counted_quantity": 0,
        "validated_quantity": 0,
        "validation_rejected_quantity": 0,
        "adjusted_quantity": 0,
        "adjustment_rejected_quantity": 0,
    }


def test_a_task_document_from_dom_12_still_loads():
    # tasks written before DOM-13 carry the stage counters but no done ones
    dom12 = {
        "total_quantity": 10,
        "counted_quantity": 4,
        "resolved_quantity": 1,
        "pending_quantity": 6,
        "second_count_quantity": 3,
        "validation_quantity": 0,
        "adjustment_quantity": 0,
    }
    lines = min_models.CountLinesQuantitiesMin(**dom12)
    assert (lines.second_counted_quantity, lines.validated_quantity, lines.adjusted_quantity) == (0, 0, 0)
    assert (lines.validation_rejected_quantity, lines.adjustment_rejected_quantity) == (0, 0)


def test_a_task_document_without_the_new_counters_still_loads():
    # tasks written before DOM-12 only carry the three original counters
    old = {"total_quantity": 10, "counted_quantity": 4, "resolved_quantity": 1}
    assert min_models.CountLinesQuantitiesMin(**old).pending_quantity == 0


def test_every_open_status_has_a_counter_and_final_statuses_have_none():
    assert set(LineStatus) - set(LINE_STAGE_COUNTERS) == FINAL_STATUSES
    fields = set(min_models.CountLinesQuantitiesMin.__dataclass_fields__)
    assert set(LINE_STAGE_COUNTERS.values()) <= fields


def test_done_and_rejected_counters_are_fields_and_pending_has_none():
    fields = set(min_models.CountLinesQuantitiesMin.__dataclass_fields__)
    assert set(LINE_DONE_COUNTERS.values()) <= fields
    assert set(LINE_REJECTED_COUNTERS.values()) <= fields
    # the first count is counted by the capture commands in counted_quantity
    assert LineStatus.PENDING not in LINE_DONE_COUNTERS
    assert LineStatus.PENDING not in LINE_REJECTED_COUNTERS
    assert set(LINE_DONE_COUNTERS.values()).isdisjoint(LINE_REJECTED_COUNTERS.values())


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
        "lines.second_counted_quantity": 4,  # whatever the destination (DOM-13)
    }


def test_a_new_out_of_system_line_only_adds():
    assert line_stage_increments([(None, LineStatus.SECOND_COUNT)]) == {
        "lines.second_count_quantity": 1
    }


def test_applying_is_counted_as_adjustment():
    assert line_stage_increments([(LineStatus.ADJUSTMENT, LineStatus.APPLYING)]) == {}
    assert line_stage_increments([(LineStatus.APPLYING, LineStatus.ADJUSTED)]) == {
        "lines.adjustment_quantity": -1,
        "lines.adjusted_quantity": 1,
    }
    # returned to audit (H-13): neither done nor rejected; the adjustments
    # command subtracts `validated` on its own when the line had been validated
    assert line_stage_increments([(LineStatus.APPLYING, LineStatus.VALIDATION)]) == {
        "lines.adjustment_quantity": -1,
        "lines.validation_quantity": 1,
    }
    assert line_stage_increments([(LineStatus.ADJUSTMENT, LineStatus.VALIDATION)]) == {
        "lines.adjustment_quantity": -1,
        "lines.validation_quantity": 1,
    }


def test_audit_splits_between_validated_and_rejected():
    transitions = [
        (LineStatus.VALIDATION, LineStatus.CLOSED),
        (LineStatus.VALIDATION, LineStatus.ADJUSTMENT),
        (LineStatus.VALIDATION, LineStatus.REJECTED),
    ]
    assert line_stage_increments(transitions) == {
        "lines.validation_quantity": -3,
        "lines.adjustment_quantity": 1,
        "lines.validated_quantity": 2,
        "lines.validation_rejected_quantity": 1,
    }


def test_adjustments_split_between_adjusted_and_rejected():
    transitions = [
        (LineStatus.ADJUSTMENT, LineStatus.ADJUSTED),
        (LineStatus.ADJUSTMENT, LineStatus.ADJUSTED),
        (LineStatus.ADJUSTMENT, LineStatus.REJECTED),
    ]
    assert line_stage_increments(transitions) == {
        "lines.adjustment_quantity": -3,
        "lines.adjusted_quantity": 2,
        "lines.adjustment_rejected_quantity": 1,
    }


def test_the_first_count_adds_no_done_counter():
    # counted_quantity is incremented by the capture commands themselves
    assert "lines.second_counted_quantity" not in line_stage_increments(
        [(LineStatus.PENDING, LineStatus.SECOND_COUNT), (LineStatus.PENDING, LineStatus.CLOSED)]
    )


def test_statuses_are_accepted_as_strings_and_empty_batches_add_nothing():
    assert line_stage_increments([("VALIDATION", "REJECTED")]) == {
        "lines.validation_quantity": -1,
        "lines.validation_rejected_quantity": 1,
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
    assert counters["second_counted_quantity"] == 3
    apply([(adjustment, LineStatus.APPLYING)])
    apply([(LineStatus.APPLYING, LineStatus.ADJUSTED)], resolved=1)
    assert (counters["adjustment_quantity"], counters["adjusted_quantity"]) == (0, 1)


def test_done_counters_follow_the_front_example():
    """5 lines with two counts: 3 to audit, 2 straight to adjustment (DOM-13 §3).
    The auditor validates 2 (1 closes, 1 to adjustment) and rejects 1; returns
    one validated line to audit (the command subtracts `validated` itself),
    validates it again; then applies 2 and rejects 1."""
    counters = asdict(
        min_models.CountLinesQuantitiesMin(total_quantity=5, pending_quantity=5)
    )

    def apply(transitions, resolved=0, counted=0, re_validated=0):
        for key, delta in line_stage_increments(transitions).items():
            counters[key.removeprefix("lines.")] += delta
        counters["resolved_quantity"] += resolved
        counters["counted_quantity"] += counted
        counters["validated_quantity"] -= re_validated

    def snapshot():
        return tuple(
            counters[name]
            for name in (
                "validation_quantity",
                "adjustment_quantity",
                "resolved_quantity",
                "validated_quantity",
                "validation_rejected_quantity",
                "adjusted_quantity",
                "adjustment_rejected_quantity",
            )
        )

    pending, second, audit, adjustment = (
        LineStatus.PENDING,
        LineStatus.SECOND_COUNT,
        LineStatus.VALIDATION,
        LineStatus.ADJUSTMENT,
    )
    apply([(pending, second)] * 5, counted=5)
    apply([(second, audit)] * 3 + [(second, adjustment)] * 2)
    assert counters["second_counted_quantity"] == 5
    assert snapshot() == (3, 2, 0, 0, 0, 0, 0)
    apply([(audit, LineStatus.CLOSED), (audit, adjustment), (audit, LineStatus.REJECTED)], resolved=2)
    assert snapshot() == (0, 3, 2, 2, 1, 0, 0)
    apply([(adjustment, audit)], re_validated=1)  # it had round 3: the command subtracts
    assert snapshot() == (1, 2, 2, 1, 1, 0, 0)
    apply([(audit, adjustment)])
    assert snapshot() == (0, 3, 2, 2, 1, 0, 0)
    apply([(adjustment, LineStatus.ADJUSTED)] * 2 + [(adjustment, LineStatus.REJECTED)], resolved=3)
    assert snapshot() == (0, 0, 5, 2, 1, 2, 1)
    assert counters["resolved_quantity"] == counters["total_quantity"]
