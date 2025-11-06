from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class LocationContentRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_item(
        self,
        search_str: str,
        *,
        page: int,
        limit: int,
        sort: Optional[List[Tuple[str, int]]] = None,
        umu_id: Optional[str] = None,
        expiration_date_gt: Optional[int] = None,
        expiration_date_lt: Optional[int] = None,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        lot: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
