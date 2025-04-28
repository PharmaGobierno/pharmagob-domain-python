from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class DispatchRecordRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_reference(
        self,
        reference_id: str,
        *,
        created_at_gt: int,
        created_at_lt: int,
        page: int,
        limit: int,
        umu_id: Optional[str] = None,
        dispatch_gt: Optional[int] = None,
        dispatch_lt: Optional[int] = None,
        service: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
