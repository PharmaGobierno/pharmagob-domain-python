from abc import abstractmethod
from typing import List, Optional

from ._base import BaseRepositoryInterface


class InventoryCountScheduleRepositoryInterface(BaseRepositoryInterface):
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
