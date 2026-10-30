import pytest

from pharmagob.v1.models.inventory_count_line import LineStatus
from pharmagob.v1.services.inventory_count_rules import CountEntry, evaluate

OUT_OF_SYSTEM = None

# Requirement v2 cases: (case, kardex, first, second, expected round 1, expected round 2)
# Each expected value is (status, case returned by the engine). Equivalent cases
# return their representative: 8 -> 7, 6 -> 5, 1 -> 13, 11 -> 2.
CASES = [
    (1, 100, 50, 100, (LineStatus.SECOND_COUNT, 3), (LineStatus.CLOSED, 13)),
    (2, 100, 50, 50, (LineStatus.SECOND_COUNT, 3), (LineStatus.ADJUSTMENT, 2)),
    (3, 100, 50, None, (LineStatus.SECOND_COUNT, 3), None),
    (4, OUT_OF_SYSTEM, 150, 150, (LineStatus.SECOND_COUNT, 5), (LineStatus.ADJUSTMENT, 4)),
    (5, OUT_OF_SYSTEM, 150, None, (LineStatus.SECOND_COUNT, 5), None),
    (6, OUT_OF_SYSTEM, 130, None, (LineStatus.SECOND_COUNT, 5), None),
    (7, 100, 100, None, (LineStatus.CLOSED, 7), None),
    (8, 100, 100, None, (LineStatus.CLOSED, 7), None),
    (9, 100, 0, 0, (LineStatus.SECOND_COUNT, 9), (LineStatus.ADJUSTMENT, 9)),
    (10, 100, 200, 200, (LineStatus.SECOND_COUNT, 10), (LineStatus.ADJUSTMENT, 10)),
    (11, 100, 80, 80, (LineStatus.SECOND_COUNT, 3), (LineStatus.ADJUSTMENT, 2)),
    (12, OUT_OF_SYSTEM, 130, 170, (LineStatus.SECOND_COUNT, 5), (LineStatus.VALIDATION, 12)),
    (13, 100, 50, 100, (LineStatus.SECOND_COUNT, 3), (LineStatus.CLOSED, 13)),
    (14, 100, 0, 10, (LineStatus.SECOND_COUNT, 9), (LineStatus.VALIDATION, 14)),
]


@pytest.mark.parametrize(
    "case, kardex, first, second, expected_first, expected_second",
    CASES,
    ids=[f"case_{c[0]}" for c in CASES],
)
def test_requirement_cases(case, kardex, first, second, expected_first, expected_second):
    is_in_system = kardex is not OUT_OF_SYSTEM
    kardex = kardex or 0
    entries = [CountEntry(first, kardex)]

    result = evaluate(entries, is_in_system=is_in_system)
    assert (result.status, result.case) == expected_first

    if second is None:
        return
    entries.append(CountEntry(second, kardex))
    result = evaluate(entries, is_in_system=is_in_system)
    assert (result.status, result.case) == expected_second


def _run_case(case):
    _, kardex, first, second, _, _ = next(c for c in CASES if c[0] == case)
    is_in_system = kardex is not OUT_OF_SYSTEM
    entries = [CountEntry(first, kardex or 0)]
    if second is not None:
        entries.append(CountEntry(second, kardex or 0))
    result = evaluate(entries, is_in_system=is_in_system)
    return result.status, result.case


@pytest.mark.parametrize("case, equivalent", [(7, 8), (5, 6), (1, 13), (2, 11)])
def test_equivalent_cases_share_outcome(case, equivalent):
    # Compares engine outputs, not rows of the CASES table
    assert _run_case(case) == _run_case(equivalent)


def test_without_entries_stays_pending():
    result = evaluate([])
    assert result.status == LineStatus.PENDING
    assert result.case is None


def test_kardex_change_between_rounds_compares_differences():
    # D-01: kardex 100, first count 50 (-50); a prescription of 10 is dispatched
    # (kardex 90) and the second count finds 40: the difference is still -50.
    entries = [CountEntry(50, 100), CountEntry(40, 90)]
    result = evaluate(entries)
    assert (result.status, result.case) == (LineStatus.ADJUSTMENT, 2)


def test_second_round_matching_moved_kardex_closes():
    entries = [CountEntry(50, 100), CountEntry(90, 90)]
    result = evaluate(entries)
    assert (result.status, result.case) == (LineStatus.CLOSED, 13)


def test_validated_round_equal_to_kardex_closes_and_keeps_case():
    entries = [CountEntry(0, 100), CountEntry(10, 100), CountEntry(100, 100)]
    result = evaluate(entries)
    assert result.status == LineStatus.CLOSED
    assert result.case is None


def test_validated_round_different_from_kardex_goes_to_adjustment():
    entries = [CountEntry(0, 100), CountEntry(10, 100), CountEntry(10, 100)]
    result = evaluate(entries)
    assert result.status == LineStatus.ADJUSTMENT
    assert result.case is None


def test_returned_to_audit_evaluates_the_last_validated_round():
    # H-13 / H-15: round 3 (validated) finds -90 -> ADJUSTMENT; the stock is not
    # enough for the $inc and the line returns to audit; a receipt arrives
    # (kardex 150) and round 4 matches the kardex -> CLOSED, not round 3 again.
    entries = [CountEntry(0, 100), CountEntry(10, 100), CountEntry(10, 100)]
    assert evaluate(entries).status == LineStatus.ADJUSTMENT
    entries.append(CountEntry(150, 150))
    result = evaluate(entries)
    assert (result.status, result.case) == (LineStatus.CLOSED, None)


def test_returned_to_audit_new_difference_goes_back_to_adjustment():
    entries = [CountEntry(0, 100), CountEntry(10, 100), CountEntry(10, 100), CountEntry(140, 150)]
    result = evaluate(entries)
    assert (result.status, result.case) == (LineStatus.ADJUSTMENT, None)
