from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class LocationContentRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_item(
        self,
        item_id: str,
        *,
        created_at_gt: int,
        created_at_lt: int,
        page: int,
        limit: int,
        umu_id: Optional[str] = None,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        lot: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
