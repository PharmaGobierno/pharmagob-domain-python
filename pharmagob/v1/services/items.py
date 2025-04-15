from typing import Iterator, List, Optional, Tuple

from pharmagob.v1.models.item import ItemModel
from pharmagob.v1.repository_interfaces.items import ItemRepositoryInterface

from ._base import BaseService


class ItemService(BaseService[ItemModel, ItemRepositoryInterface]):
    __model__ = ItemModel

    def __init__(self, repository: ItemRepositoryInterface):
        super().__init__(repository)

    def paginated_query(
        self,
        conditions: Optional[List[tuple]] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
    ) -> Tuple[int, Iterator[dict]]:
        count, query_result = self.repository.query_paginated(
            page=page, limit=limit, and_conditions=conditions, sort=sort
        )
        return count, query_result
