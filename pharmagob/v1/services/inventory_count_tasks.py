from time import time
from typing import Dict, Iterable, Iterator, List, Optional, Tuple, Union

from pharmagob.v1.models.inventory_count_line import LineStatus
from pharmagob.v1.models.inventory_count_task import InventoryCountTaskModel, TaskStatus
from pharmagob.v1.repository_interfaces.inventory_count_tasks import (
    InventoryCountTaskRepositoryInterface,
)

from ._base import UmuScopedService


# Task counter that holds the lines of each open line status (DOM-12). The
# final statuses (CLOSED, ADJUSTED, REJECTED) have no stage counter: they are
# counted in `lines.resolved_quantity` by whoever resolves the line.
LINE_STAGE_COUNTERS: Dict[LineStatus, str] = {
    LineStatus.PENDING: "pending_quantity",
    LineStatus.SECOND_COUNT: "second_count_quantity",
    LineStatus.VALIDATION: "validation_quantity",
    LineStatus.ADJUSTMENT: "adjustment_quantity",
    LineStatus.APPLYING: "adjustment_quantity",
}

# Task counter that accumulates the lines that LEFT each open status forward
# (DOM-13): "done" is the next stage, whatever it is. PENDING has none because
# `lines.counted_quantity` is incremented by the capture commands themselves.
LINE_DONE_COUNTERS: Dict[LineStatus, str] = {
    LineStatus.SECOND_COUNT: "second_counted_quantity",
    LineStatus.VALIDATION: "validated_quantity",
    LineStatus.ADJUSTMENT: "adjusted_quantity",
    LineStatus.APPLYING: "adjusted_quantity",
}

# Task counter that accumulates the lines that left each status REJECTED
# (DOM-13): a rejection is never "done", it has its own counter per origin.
LINE_REJECTED_COUNTERS: Dict[LineStatus, str] = {
    LineStatus.VALIDATION: "validation_rejected_quantity",
    LineStatus.ADJUSTMENT: "adjustment_rejected_quantity",
    LineStatus.APPLYING: "adjustment_rejected_quantity",
}

ADJUSTMENT_STATUSES = {LineStatus.ADJUSTMENT, LineStatus.APPLYING}

LineStatusLike = Union[LineStatus, str]


def _done_counter(previous: LineStatus, new: LineStatus) -> Optional[str]:
    """Done or rejected counter a transition adds to, if any (DOM-13).

    From ADJUSTMENT the only forward exit is ADJUSTED: `-> APPLYING` is the
    claim of the same stage and `-> VALIDATION` is a return to audit, which
    the adjustments command handles on its own (it subtracts `validated`
    only when the line had been validated)."""
    if new == LineStatus.REJECTED:
        return LINE_REJECTED_COUNTERS.get(previous)
    if previous in ADJUSTMENT_STATUSES:
        return LINE_DONE_COUNTERS[previous] if new == LineStatus.ADJUSTED else None
    return LINE_DONE_COUNTERS.get(previous)


def line_stage_increments(
    transitions: Iterable[Tuple[Optional[LineStatusLike], Optional[LineStatusLike]]],
) -> Dict[str, int]:
    """Increments of the stage, done and rejected counters of a task for a
    batch of line status changes, ready to merge into
    `InventoryCountTaskService.increment`.

    Each transition is `(previous_status, new_status)`; `None` as previous
    status is a line that did not exist (out of system). Counters whose net
    change is zero are left out, so `ADJUSTMENT -> APPLYING` adds nothing.

    >>> line_stage_increments([("PENDING", "SECOND_COUNT"), ("PENDING", "CLOSED")])
    {'lines.pending_quantity': -2, 'lines.second_count_quantity': 1}
    >>> line_stage_increments([("VALIDATION", "ADJUSTMENT"), ("VALIDATION", "REJECTED")])
    {'lines.validation_quantity': -2, 'lines.adjustment_quantity': 1, 'lines.validated_quantity': 1, 'lines.validation_rejected_quantity': 1}
    """
    deltas: Dict[str, int] = {}
    for previous, new in transitions:
        previous = LineStatus(previous) if previous is not None else None
        new = LineStatus(new) if new is not None else None
        for status, step in ((previous, -1), (new, 1)):
            if status is None:
                continue
            counter = LINE_STAGE_COUNTERS.get(status)
            if counter is not None:
                deltas[counter] = deltas.get(counter, 0) + step
        if previous is None or new is None or previous == new:
            continue
        done = _done_counter(previous, new)
        if done is not None:
            deltas[done] = deltas.get(done, 0) + 1
    return {f"lines.{name}": delta for name, delta in deltas.items() if delta != 0}


class InventoryCountTaskService(
    UmuScopedService[InventoryCountTaskModel, InventoryCountTaskRepositoryInterface]
):
    __model__ = InventoryCountTaskModel

    def claim(
        self,
        entity_id: str,
        *,
        expected_statuses: List[TaskStatus],
        data: dict,
        umu_id: str,
    ) -> Optional[InventoryCountTaskModel]:
        result = self.repository.claim(
            entity_id,
            expected_statuses=expected_statuses,
            data={**data, "updated_at": round(time() * 1000)},
            umu_id=umu_id,
        )
        if not result:
            return None
        return InventoryCountTaskModel(**result)

    def increment(
        self,
        entity_id: str,
        *,
        quantities: Dict[str, int],
        umu_id: str,
    ) -> int:
        return self.repository.increment(
            entity_id, quantities=quantities, umu_id=umu_id
        )

    def search_by_task_name(
        self,
        search_str: str,
        *,
        umu_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        count_type: Optional[str] = None,
        status: Optional[List[str]] = None,
        cyclic_mode: Optional[str] = None,
        scheduled_at_gt: Optional[int] = None,
        scheduled_at_lt: Optional[int] = None,
    ) -> Tuple[int, Iterator[InventoryCountTaskModel]]:
        count, result = self.repository.search_by_task_name(
            search_str,
            umu_id=umu_id,
            count_type=count_type,
            status=status,
            cyclic_mode=cyclic_mode,
            scheduled_at_gt=scheduled_at_gt,
            scheduled_at_lt=scheduled_at_lt,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: InventoryCountTaskModel(**r), result)

    def search_by_reference_id(
        self,
        search_str: str,
        *,
        umu_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        count_type: Optional[str] = None,
        status: Optional[List[str]] = None,
        cyclic_mode: Optional[str] = None,
        scheduled_at_gt: Optional[int] = None,
        scheduled_at_lt: Optional[int] = None,
    ) -> Tuple[int, Iterator[InventoryCountTaskModel]]:
        count, result = self.repository.search_by_reference_id(
            search_str,
            umu_id=umu_id,
            count_type=count_type,
            status=status,
            cyclic_mode=cyclic_mode,
            scheduled_at_gt=scheduled_at_gt,
            scheduled_at_lt=scheduled_at_lt,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: InventoryCountTaskModel(**r), result)
