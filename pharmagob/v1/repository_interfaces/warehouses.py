from abc import abstractmethod
from typing import Dict, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class WarehouseRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
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
        sort: Optional[Dict[str, int]] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
