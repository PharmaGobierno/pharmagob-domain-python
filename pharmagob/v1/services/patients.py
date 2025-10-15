from typing import Iterator, Optional, Tuple

from pharmagob.v1.models.patient import PatientModel
from pharmagob.v1.repository_interfaces.patients import PatientRepositoryInterface

from ._base import BaseService


class PatientService(BaseService[PatientModel, PatientRepositoryInterface]):
    __model__ = PatientModel

    def search_by_curp(
        self,
        curp: str,
        *,
        umu_id: str,
        page: int,
        limit: int,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
    ) -> Tuple[int, Iterator[PatientModel]]:
        count, result = self.repository.search_by_curp(
            curp,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            page=page,
            limit=limit,
            umu_id=umu_id,
        )
        return count, map(lambda r: PatientModel(**r), result)

    def search_by_full_name(
        self,
        full_name: str,
        *,
        umu_id: str,
        page: int,
        limit: int,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
    ) -> Tuple[int, Iterator[PatientModel]]:
        count, result = self.repository.search_by_full_name(
            full_name,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            page=page,
            limit=limit,
            umu_id=umu_id,
        )
        return count, map(lambda r: PatientModel(**r), result)
