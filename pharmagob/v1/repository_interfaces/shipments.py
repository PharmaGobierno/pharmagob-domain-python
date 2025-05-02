from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class ShipmentRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_order_number(
        self,
        order_number: str,
        *,
        page: int,
        limit: int,
        umu_id: Optional[str] = None,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
        review_status: Optional[List[str]] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
