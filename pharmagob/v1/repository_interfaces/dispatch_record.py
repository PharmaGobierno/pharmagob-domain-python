from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class DispatchRecordRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_reference(
        self,
        reference_id: str,
        *,
        page: int,
        limit: int,
        umu_id: Optional[str] = None,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
        dispatch_at_gt: Optional[int] = None,
        dispatch_at_lt: Optional[int] = None,
        service: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
