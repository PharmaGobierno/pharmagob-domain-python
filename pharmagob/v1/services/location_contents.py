from typing import Iterator, Optional, Tuple

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
        item_id: str,
        *,
        umu_id: str,
        page: int,
        limit: int,
        quantity_gt: Optional[int] = None,
        quantity_lt: Optional[int] = None,
        expiration_date_gt: Optional[int] = None,
        expiration_date_lt: Optional[int] = None,
        lot: Optional[str] = None
    ) -> Tuple[int, Iterator[LocationContentModel]]:
        count, result = self.repository.search_by_item(
            item_id,
            expiration_date_gt=expiration_date_gt,
            expiration_date_lt=expiration_date_lt,
            page=page,
            limit=limit,
            umu_id=umu_id,
            quantity_gt=quantity_gt,
            quantity_lt=quantity_lt,
            lot=lot,
        )
        return count, map(lambda r: LocationContentModel(**r), result)
