from abc import abstractmethod
from typing import Dict, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class InventoryCountTaskRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_task_name(
        self,
        search_str: str,
        *,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        umu_id: Optional[str] = None,
        count_type: Optional[str] = None,
        status: Optional[List[str]] = None,
        cyclic_mode: Optional[str] = None,
        scheduled_at_gt: Optional[int] = None,
        scheduled_at_lt: Optional[int] = None,
    ) -> Tuple[int, List[dict]]:
        """Partial match, case and accent insensitive."""
        raise NotImplementedError

    @abstractmethod
    def search_by_reference_id(
        self,
        search_str: str,
        *,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        umu_id: Optional[str] = None,
        count_type: Optional[str] = None,
        status: Optional[List[str]] = None,
        cyclic_mode: Optional[str] = None,
        scheduled_at_gt: Optional[int] = None,
        scheduled_at_lt: Optional[int] = None,
    ) -> Tuple[int, List[dict]]:
        """Exact match of the folio."""
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
        """Atomically $set `data` only if the task status is one of
        `expected_statuses` (find_one_and_update). Returns the updated
        document, or None when another request already moved the task."""
        raise NotImplementedError

    @abstractmethod
    def increment(
        self,
        entity_id: str,
        *,
        quantities: Dict[str, int],
        umu_id: Optional[str] = None,
    ) -> int:
        """$inc the given counters, e.g. {"lines.counted_quantity": 1}.
        Returns the number of modified documents."""
        raise NotImplementedError
