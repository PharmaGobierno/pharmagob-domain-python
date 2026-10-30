from abc import abstractmethod
from typing import Dict, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class InventoryCountEventRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_reference_id(
        self,
        search_str: str,
        *,
        created_at_gt: int,
        created_at_lt: int,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        umu_id: Optional[str] = None,
        event: Optional[List[str]] = None,
        author_id: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        """Search by task folio (task.reference_id); the date range is
        mandatory, same as the audit trail listing."""
        raise NotImplementedError
