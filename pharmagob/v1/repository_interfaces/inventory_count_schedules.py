from abc import abstractmethod
from typing import Dict, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class InventoryCountScheduleRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_schedule_name(
        self,
        search_str: str,
        *,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        umu_id: Optional[str] = None,
        status: Optional[str] = None,
        frequency: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        """Partial match, case and accent insensitive."""
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
        """Atomically $set `data` only if the schedule status is one of
        `expected_statuses` (find_one_and_update). Returns the updated
        document, or None when another tick already claimed it."""
        raise NotImplementedError
