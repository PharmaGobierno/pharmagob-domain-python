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
        created_at_gt: int,
        created_at_lt: int,
        page: int,
        limit: int,
        lot: Optional[str] = None
    ) -> Tuple[int, Iterator[LocationContentModel]]:
        count, result = self.repository.search_by_item(
            item_id,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            page=page,
            limit=limit,
            umu_id=umu_id,
            lot=lot,
        )
        return count, map(lambda r: LocationContentModel(**r), result)
