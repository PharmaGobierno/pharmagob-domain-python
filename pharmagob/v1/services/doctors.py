from typing import Iterator, Optional, Tuple

from pharmagob.v1.models.doctor import DoctorModel
from pharmagob.v1.repository_interfaces.doctors import DoctorRepositoryInterface

from ._base import BaseService


class DoctorService(BaseService[DoctorModel, DoctorRepositoryInterface]):
    __model__ = DoctorModel

    def search_by_employee_or_licence(
        self,
        employee_number: str,
        *,
        umu_id: str,
        created_at_gt: int,
        created_at_lt: int,
        page: int,
        limit: int,
    ) -> Tuple[int, Iterator[DoctorModel]]:
        count, result = self.repository.search_by_employee_or_licence(
            employee_number,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            page=page,
            limit=limit,
            umu_id=umu_id,
        )
        return count, map(lambda r: DoctorModel(**r), result)
