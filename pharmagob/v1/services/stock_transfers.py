from typing import Dict, Iterator, Optional, Tuple

from pharmagob.v1.models.stock_transfer import StockTransferModel
from pharmagob.v1.repository_interfaces.stock_transfers import (
    StockTransferRepositoryInterface,
)

from ._base import BaseService


class StockTransferService(
    BaseService[StockTransferModel, StockTransferRepositoryInterface]
):
    __model__ = StockTransferModel

    def search_by_reference_id(
        self,
        search_str: str,
        *,
        page: int = 1,
        limit: int = 50,
        sort: Optional[Dict[str, int]] = None,
        last_event: Optional[str] = None,
        umu_id: Optional[str] = None,
        foreign_umu_id: Optional[str] = None,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
    ) -> Tuple[int, Iterator[StockTransferModel]]:
        count, result = self.repository.search_by_reference_id(
            search_str,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            umu_id=umu_id,
            last_event=last_event,
            foreign_umu_id=foreign_umu_id,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: StockTransferModel(**r), result)
