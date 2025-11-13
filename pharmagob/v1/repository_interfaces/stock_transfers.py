from abc import abstractmethod
from typing import Dict, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class StockTransferRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_reference_id(
        self,
        search_str: str,
        *,
        page: int = 1,
        limit: int = 50,
        sort: Optional[Dict[str, int]] = None,
        last_event: Optional[str] = None,
        umu_id: Optional[str] = None,
        foreign_umu_id: Optional[str] = None,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
