from typing import List, Optional, Tuple
from ._base import BaseRepositoryInterface
from abc import abstractmethod


class WarehouseRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_umu(
        self,
        search_str: str,
        *,
        page: int,
        limit: int,
        type: Optional[str] = None,
        disable: Optional[bool] = None
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
