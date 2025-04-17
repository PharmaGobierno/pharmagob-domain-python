from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class ShipmentRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def sarch_by_order_number(
        self,
        order_number: str,
        *,
        created_at_gt: int,
        created_at_lt: int,
        page: int,
        limit: int,
        review_status: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
