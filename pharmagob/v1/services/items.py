from typing import Iterator, List, Optional, Tuple, Union

from pharmagob.v1.models.item import ItemModel
from pharmagob.v1.repository_interfaces.items import ItemRepositoryInterface

from ._base import BaseService


class ItemService(BaseService[ItemModel, ItemRepositoryInterface]):
    __model__ = ItemModel

    def get_by_foreign_id(
        self,
        foreign_id,
        *,
        umu_id: Optional[str] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None,
        limit: Optional[int] = None,
    ) -> Tuple[int, Iterator[ItemModel]]:
        count, result = self.repository.get_by_foreign_id(
            foreign_id, sort=sort, umu_id=umu_id, projection=projection, limit=limit
        )
        return count, map(lambda r: ItemModel(**r), result)
