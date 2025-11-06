from typing import Iterator, List, Optional, Tuple, Union

from pharmagob.v1.models.stock_transfer_event import StockTransferEventModel
from pharmagob.v1.repository_interfaces.stock_transfer_events import (
    StockTransferEventRepositoryInterface,
)

from ._base import BaseService


class StockTransferEventService(
    BaseService[StockTransferEventModel, StockTransferEventRepositoryInterface]
):
    __model__ = StockTransferEventModel

    def get_by_stock_transfer_id(
        self,
        stock_transfer_id: str,
        *,
        umu_id: Optional[str] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None,
        limit: Optional[int] = None,
    ) -> Tuple[int, Iterator[StockTransferEventModel]]:
        count, result = self.repository.get_by_stock_transfer_id(
            stock_transfer_id,
            umu_id=umu_id,
            sort=sort,
            limit=limit,
            projection=projection,
        )
        return count, map(lambda r: StockTransferEventModel(**r), result)
