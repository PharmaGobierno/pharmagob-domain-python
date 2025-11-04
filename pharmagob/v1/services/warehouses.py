from typing import Iterator, Optional, Tuple

from pharmagob.v1.models.warehouse import WarehouseModel
from pharmagob.v1.repository_interfaces.warehouses import WarehouseRepositoryInterface

from ._base import BaseService


class WarehouseService(BaseService[WarehouseModel, WarehouseRepositoryInterface]):
    __model__ = WarehouseModel

    def search_by_umu(
        self,
        search_str: str,
        *,
        page: int,
        limit: int,
        type: Optional[str] = None,
        disable: Optional[bool] = None,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
        sort_order: int = -1,
    ) -> Tuple[int, Iterator[WarehouseModel]]:
        count, result = self.repository.search_by_umu(
            search_str,
            page=page,
            limit=limit,
            type=type,
            disable=disable,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            sort_order=sort_order,
        )
        return count, map(lambda r: WarehouseModel(**r), result)
