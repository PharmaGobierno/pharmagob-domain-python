from abc import abstractmethod
from typing import Dict, List, Optional

from ._base import BaseRepositoryInterface


class InventoryCountTaskRepositoryInterface(BaseRepositoryInterface):
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
