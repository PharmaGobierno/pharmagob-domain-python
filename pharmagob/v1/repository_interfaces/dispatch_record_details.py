from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class DispatchRecordDetailRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def get_by_dispatch_record_id(
        self,
        dispatch_record_id: str,
        *,
        umu_id: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
