from abc import abstractmethod
from typing import List, Optional, Tuple

from ._base import BaseRepositoryInterface


class DoctorRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def search_by_employee_or_licence(
        self,
        employee_number: str,
        *,
        page: int,
        limit: int,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
        umu_id: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError

    @abstractmethod
    def search_by_full_name(
        self,
        full_name: str,
        *,
        page: int,
        limit: int,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
        umu_id: Optional[str] = None,
    ) -> Tuple[int, List[dict]]:
        raise NotImplementedError
