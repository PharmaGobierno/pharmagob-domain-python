from abc import abstractmethod
from typing import Any, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class InventoryCountLineRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def claim(
        self,
        entity_id: str,
        *,
        expected_statuses: List[str],
        data: dict,
        umu_id: Optional[str] = None,
    ) -> Optional[dict]:
        """Atomically $set `data` only if the line status is one of
        `expected_statuses` (e.g. ADJUSTMENT -> APPLYING). Returns the
        updated document, or None when another request already claimed it."""
        raise NotImplementedError

    @abstractmethod
    def insert_many_ignore_duplicates(self, data: List[dict]) -> Tuple[int, int, int]:
        """insert_many(ordered=False) that classifies duplicate key errors
        instead of raising them.

        Returns:
            (inserted, duplicated, locked): `duplicated` collided on the line
            _id (redelivery or repeated key in the same task) and `locked`
            collided on the {umu_id, task.count_type, location_content_id}
            partial unique index (open in another task of the same type, D-02).
        """
        raise NotImplementedError

    @abstractmethod
    def soft_delete_by_task(
        self,
        task_id: str,
        *,
        deleted_at: int,
        umu_id: Optional[str] = None,
    ) -> int:
        """Mark every line of the task with `deleted_at` and `is_open=False`
        (releases the D-02 lock) without removing documents (D-09).
        Returns the number of modified documents."""
        raise NotImplementedError

    @abstractmethod
    def delete_many(
        self,
        and_conditions: Optional[List[Tuple[str, str, Any]]],
        *,
        limit: Optional[int] = None,
    ) -> int:
        """Physically delete up to `limit` matching documents, used by the
        deferred purge of soft-deleted lines (D-09). Returns the number of
        deleted documents."""
        raise NotImplementedError
