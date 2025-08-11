from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class PatientRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_curp(
        self,
        curp: str,
        *,
        page: int,
        limit: int,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
        umu_id: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
