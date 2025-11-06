from abc import abstractmethod
from typing import Iterator, List, Optional, Tuple, Union

from ._base import BaseRepositoryInterface


class StockTransferEventRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def get_by_stock_transfer_id(
        self,
        stock_transfer_id: str,
        *,
        umu_id: Optional[str] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        limit: Optional[int] = None,
        projection: Optional[Union[list, dict]] = None,
    ) -> Tuple[int, Iterator[dict]]:
        raise NotImplementedError
