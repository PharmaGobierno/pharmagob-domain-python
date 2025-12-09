from abc import abstractmethod
from typing import Dict, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class LocationContentRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_item(
        self,
        search_str: str,
        *,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        umu_id: Optional[str] = None,
        expiration_date_gt: Optional[int] = None,
        expiration_date_lt: Optional[int] = None,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        lot: Optional[str] = None,
        location_id: Optional[str] = None,
        location_label_code: Optional[str] = None
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError

    @abstractmethod
    def search_by_item_global(
        self,
        search_str: str,
        *,
        page: int,
        limit: int,
        sort: Optional[Dict[str, int]] = None,
        umu_id_in: Optional[List[str]] = None,
        umu_id_not_in: Optional[List[str]] = None,
        expiration_date_gt: Optional[int] = None,
        expiration_date_lt: Optional[int] = None,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        lot: Optional[str] = None,
        location_id: Optional[str] = None,
        location_label_code: Optional[str] = None
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
