from abc import abstractmethod
from typing import Dict, List, Optional, Tuple, Any

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
        location_label_code: Optional[str] = None,
        location_label_code_not_in: Optional[List[str]] = None
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

    @abstractmethod
    def trigger_report_aggregation(
        self, report_id: str, filters: Dict[str, Any]
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def find_by_logic_triad(
        self, item_id: str, lot: str, location_id: str
    ) -> Optional[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_by_ids(
        self,
        entity_ids: List[str],
        umu_id: str,
    ) -> List[dict]:
        raise NotImplementedError

    @abstractmethod
    def get_batch_after(
        self,
        umu_id: str,
        *,
        after_id: Optional[str] = None,
        limit: int = 1000,
        location_label_code: Optional[str] = None,
        location_label_code_not_in: Optional[List[str]] = None,
        quantity_gt: Optional[int] = None,
        item_ids: Optional[List[str]] = None,
    ) -> List[dict]:
        """Keyset (cursor) read sorted by _id ascending: returns up to `limit`
        documents with _id > `after_id`. Used by the inventory count line
        creation instead of skip/limit pagination."""
        raise NotImplementedError

    @abstractmethod
    def increment_quantity(
        self,
        location_content_id: str,
        delta: int,
        *,
        last_author: dict,
        updated_at: int,
        min_quantity: Optional[int] = None,
        umu_id: Optional[str] = None,
    ) -> Optional[dict]:
        """Atomic `$inc` of quantity (find_one_and_update). Returns the
        document AFTER the change, or None when nothing matched (it does not
        exist, belongs to another UMU, or has less than `min_quantity`).
        A decrement requires `min_quantity >= abs(delta)` so stock never goes
        negative; otherwise it raises ValueError."""
        raise NotImplementedError

    @abstractmethod
    def upsert_increment_quantity(
        self,
        location_content_id: str,
        delta: int,
        *,
        insert_data: dict,
        last_author: dict,
        updated_at: int,
    ) -> dict:
        """Creates the location content with quantity = `delta` (the rest of
        `insert_data` is written only on insert) or adds `delta` to the
        existing one. `delta` must be > 0. Returns the document AFTER."""
        raise NotImplementedError
