from time import time
from typing import Optional

from pharmagob.v1.repository_interfaces.reference_counters import (
    ReferenceCounterRepositoryInterface,
)

DEFAULT_REFERENCE_WIDTH = 6  # CF-000001


class ReferenceCounterService:
    """Global consecutive references (D-03): `next` returns the sequence
    number and `next_reference_id` formats it as `<prefix>-<seq:06d>`.
    Only the create endpoints call it; a taken number is consumed even if
    the entity is cancelled later (D-09), gaps are accepted."""

    def __init__(self, repository: ReferenceCounterRepositoryInterface):
        self.repository = repository

    def next(self, entity: str, prefix: str, scope: Optional[str] = None) -> int:
        return self.repository.next_sequence(
            entity, prefix, scope=scope, updated_at=round(time() * 1000)
        )

    def next_reference_id(
        self,
        entity: str,
        prefix: str,
        scope: Optional[str] = None,
        *,
        width: int = DEFAULT_REFERENCE_WIDTH,
    ) -> str:
        seq = self.next(entity, prefix, scope)
        return self.format_reference_id(prefix, seq, width=width)

    @staticmethod
    def format_reference_id(prefix: str, seq: int, *, width: int = DEFAULT_REFERENCE_WIDTH) -> str:
        return f"{prefix}-{seq:0{width}d}"
