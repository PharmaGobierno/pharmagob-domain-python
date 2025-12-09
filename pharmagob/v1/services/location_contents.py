from typing import Dict, Iterator, List, Optional, Tuple

from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.repository_interfaces.location_contents import (
    LocationContentRepositoryInterface,
)

from ._base import BaseService


class LocationContentService(
    BaseService[LocationContentModel, LocationContentRepositoryInterface]
):
    __model__ = LocationContentModel

    def search_by_item(
        self,
        search_str: str,
        *,
        umu_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        expiration_date_gt: Optional[int] = None,
        expiration_date_lt: Optional[int] = None,
        lot: Optional[str] = None
    ) -> Tuple[int, Iterator[LocationContentModel]]:
        count, result = self.repository.search_by_item(
            search_str,
            expiration_date_gt=expiration_date_gt,
            expiration_date_lt=expiration_date_lt,
            umu_id=umu_id,
            quantity_gt=quantity_gt,
            quantity_lt=quantity_lt,
            lot=lot,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: LocationContentModel(**r), result)

    def search_by_item_global(
        self,
        search_str: str,
        *,
        page: int,
        limit: int,
        sort: Optional[Dict[str, int]] = None,
        umu_id_not_in: Optional[List[str]] = None,
        umu_id_in: Optional[List[str]] = None,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        expiration_date_gt: Optional[int] = None,
        expiration_date_lt: Optional[int] = None,
        lot: Optional[str] = None
    ) -> Tuple[int, Iterator[LocationContentModel]]:
        count, result = self.repository.search_by_item_global(
            search_str,
            expiration_date_gt=expiration_date_gt,
            expiration_date_lt=expiration_date_lt,
            umu_id_in=umu_id_in,
            umu_id_not_in=umu_id_not_in,
            quantity_gt=quantity_gt,
            quantity_lt=quantity_lt,
            lot=lot,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: LocationContentModel(**r), result)
