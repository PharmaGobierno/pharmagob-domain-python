from abc import ABCMeta, abstractmethod
from typing import Optional


class ReferenceCounterRepositoryInterface(metaclass=ABCMeta):
    """Port of the shared `reference-counters` collection. It is not a
    CRUD repository, so it does not extend BaseRepositoryInterface."""

    @abstractmethod
    def next_sequence(
        self,
        entity: str,
        prefix: str,
        *,
        scope: Optional[str] = None,
        updated_at: int,
    ) -> int:
        """Atomically increments and returns the next value of the
        sequence `entity:prefix[:scope]`, creating the document on first
        use: `find_one_and_update({_id: key}, {$inc: {seq: 1}, $set:
        {updated_at}, $setOnInsert: {entity, prefix, scope}}, upsert=True,
        return_document=AFTER)`. Retry once on DuplicateKeyError (two first
        uses of the same key at the same time)."""
        raise NotImplementedError
