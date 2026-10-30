from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class ReferenceCounterModel:
    """One document per sequence in the shared `reference-counters`
    collection (atomic sequence counter, epic Conteos §5.6 / D-03).

    The key is `entity:prefix[:scope]`; documents are born on first use
    with `find_one_and_update($inc, upsert=True)`, nobody seeds them. The
    scope is optional (e.g. a UMU or a year) so a sequence that one day
    needs a reset is just a new key starting at 1."""

    __entity_name__ = "reference-counters"

    _id: str
    entity: str
    prefix: str
    seq: int
    updated_at: int
    scope: Optional[str] = None

    @staticmethod
    def build_key(entity: str, prefix: str, scope: Optional[str] = None) -> str:
        parts = [entity, prefix] + ([scope] if scope else [])
        return ":".join(parts)
