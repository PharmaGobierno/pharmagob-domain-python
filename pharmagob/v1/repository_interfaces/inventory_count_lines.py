from abc import abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class InventoryCountLineRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_item(
        self,
        search_str: str,
        *,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        umu_id: Optional[str] = None,
        task_id: Optional[str] = None,
        status: Optional[List[str]] = None,
        lot: Optional[str] = None,
        is_in_system: Optional[bool] = None,
        adjustment_sign: Optional[str] = None,
        resolution_type: Optional[str] = None,
        resolution_origin: Optional[str] = None,
        resolved_at_gt: Optional[int] = None,
        resolved_at_lt: Optional[int] = None,
    ) -> Tuple[int, List[dict]]:
        """Search by item key (item.id / item.foreign_id)."""
        raise NotImplementedError

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
        updated document, or None when another request already claimed it.

        Claims of the adjustment flow (H-21, H-13 / H-15):
        - ADJUSTMENT -> APPLYING: `data` also fixes `resolution.resolved_at`,
          the stable timestamp reused by the $inc, the applied message and
          the location-content-events, so a retry does not duplicate them.
        - APPLYING -> VALIDATION (insufficient stock) or ADJUSTMENT ->
          VALIDATION (sent by the auditor): `data` clears `resolved_at`,
          does NOT write `resolution`, keeps `is_open` True and sets
          `context.returned_to_audit`.
        """
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
