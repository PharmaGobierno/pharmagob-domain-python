from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ._base import EventfulModel, uuid_by_params
from .inventory_count_task import CountType
from .minified import min_models


class Events(str, Enum):
    TASK_SCHEDULED = "TASK_SCHEDULED"
    TASK_RELEASED = "TASK_RELEASED"
    TASK_DELETED = "TASK_DELETED"
    TASK_CANCELLED = "TASK_CANCELLED"
    TASK_CLOSED = "TASK_CLOSED"
    TASK_EXPIRED = "TASK_EXPIRED"
    SCHEDULE_CREATED = "SCHEDULE_CREATED"
    SCHEDULE_ACTIVATED = "SCHEDULE_ACTIVATED"
    SCHEDULE_INACTIVATED = "SCHEDULE_INACTIVATED"
    SCHEDULE_CANCELLED = "SCHEDULE_CANCELLED"
    SCHEDULE_RUN_SKIPPED = "SCHEDULE_RUN_SKIPPED"
    COUNT_CAPTURED = "COUNT_CAPTURED"
    OUT_OF_SYSTEM_REGISTERED = "OUT_OF_SYSTEM_REGISTERED"
    AUDIT_VALIDATED = "AUDIT_VALIDATED"
    ADJUSTMENT_POSITIVE = "ADJUSTMENT_POSITIVE"
    ADJUSTMENT_NEGATIVE = "ADJUSTMENT_NEGATIVE"
    REJECTED = "REJECTED"
    # Line sent back from adjustment to audit: insufficient stock for the
    # conditional $inc (H-13) or returned by the auditor (H-15)
    ADJUSTMENT_RETURNED_TO_AUDIT = "ADJUSTMENT_RETURNED_TO_AUDIT"


CountEventType = Events  # name used in the epic


class AuditActivity(str, Enum):
    CREATION = "CREATION"
    MODIFICATION = "MODIFICATION"
    DELETION = "DELETION"


TASK_EVENTS = {
    Events.TASK_SCHEDULED,
    Events.TASK_RELEASED,
    Events.TASK_DELETED,
    Events.TASK_CANCELLED,
    Events.TASK_CLOSED,
    Events.TASK_EXPIRED,
}
# At most once per line
LINE_EVENTS = {
    Events.OUT_OF_SYSTEM_REGISTERED,
    Events.ADJUSTMENT_POSITIVE,
    Events.ADJUSTMENT_NEGATIVE,
    Events.REJECTED,
}
# Repeat when the line returns from adjustment to audit (H-13 / H-15)
REPEATABLE_LINE_EVENTS = {Events.AUDIT_VALIDATED, Events.ADJUSTMENT_RETURNED_TO_AUDIT}
SCHEDULE_EVENTS = {Events.SCHEDULE_CREATED, Events.SCHEDULE_CANCELLED}
REPEATABLE_SCHEDULE_EVENTS = {Events.SCHEDULE_ACTIVATED, Events.SCHEDULE_INACTIVATED}


@dataclass(kw_only=True)
class InventoryCountEventModel(EventfulModel[Events]):
    """Immutable audit trail entry. The _id is the deterministic event_id:
    stable business data only, the clock stays out of the identity except
    in the repeatable events."""

    __entity_name__ = "inventory-count-events"

    umu_id: str
    author: min_models.UserMin
    activity: AuditActivity
    count_type: CountType
    task: Optional[min_models.CountTaskMin] = None  # None only in schedule events
    line: Optional[min_models.CountLineMin] = None
    schedule: Optional[min_models.CountScheduleMin] = None
    initial_quantity: Optional[int] = None
    final_quantity: Optional[int] = None
    comment: Optional[str] = None
    context: dict = field(default_factory=dict)

    @classmethod
    def _dict_to_dataclasses(cls, instance):
        super()._dict_to_dataclasses(instance)
        if isinstance(instance.task, dict):
            instance.task = min_models.CountTaskMin(**instance.task)
        if isinstance(instance.line, dict):
            instance.line = min_models.CountLineMin(**instance.line)
        if isinstance(instance.schedule, dict):
            instance.schedule = min_models.CountScheduleMin(**instance.schedule)

    @classmethod
    def generate_event_id(
        cls,
        event: Events,
        *,
        task_id: Optional[str] = None,
        line_id: Optional[str] = None,
        schedule_id: Optional[str] = None,
        author_id: Optional[str] = None,
        transition_timestamp: Optional[int] = None,
        counted_at: Optional[int] = None,
        returned_at: Optional[int] = None,
        next_run_at: Optional[int] = None,
    ) -> str:
        """Deterministic event_id (epic §5.10): stable business data inside
        the id, the clock outside. The discriminators of the repeatable
        events are generated once by the publisher and saved in the line
        (`counts[].counted_at`, `context.returned_to_audit.returned_at`) or
        in the schedule (`next_run_at`), never `now()` at publish time."""
        # The enum value (not str(Enum)) keeps the id stable when the event
        # is read back from Mongo as a plain str.
        event = Events(event)
        if event in TASK_EVENTS:
            return uuid_by_params(task_id, event.value)
        if event in LINE_EVENTS:
            return uuid_by_params(line_id, event.value)
        if event == Events.AUDIT_VALIDATED:
            # counted_at of the validated round (H-13 / H-15)
            return uuid_by_params(line_id, event.value, counted_at)
        if event == Events.ADJUSTMENT_RETURNED_TO_AUDIT:
            # returned_at of context.returned_to_audit (H-13 / H-15)
            return uuid_by_params(line_id, event.value, returned_at)
        if event == Events.COUNT_CAPTURED:
            return uuid_by_params(task_id, event.value, author_id, counted_at)
        if event in SCHEDULE_EVENTS:
            return uuid_by_params(schedule_id, event.value)
        if event in REPEATABLE_SCHEDULE_EVENTS:
            return uuid_by_params(schedule_id, event.value, transition_timestamp)
        # SCHEDULE_RUN_SKIPPED: the skipped occurrence is the stable discriminator
        if next_run_at is None:
            raise ValueError("SCHEDULE_RUN_SKIPPED requires context.next_run_at")
        return uuid_by_params(schedule_id, event.value, next_run_at)

    def __post_init__(self):
        super().__post_init__()
        context = self.context or {}
        returned_to_audit = context.get("returned_to_audit") or {}
        self._id = self.generate_event_id(
            self.event,
            task_id=self.task.id if self.task else None,
            line_id=self.line.id if self.line else None,
            schedule_id=self.schedule.id if self.schedule else None,
            author_id=self.author.id,
            transition_timestamp=self.transition_timestamp,
            # The publisher sets transition_timestamp to the counted_at of
            # the saved round (COUNT_CAPTURED, AUDIT_VALIDATED)
            counted_at=context.get("counted_at", self.transition_timestamp),
            returned_at=returned_to_audit.get("returned_at", self.transition_timestamp),
            next_run_at=context.get("next_run_at"),
        )
