from typing import Iterator, Optional, Tuple

from pharmagob.v1.models.dispatch_record import DispatchRecordModel
from pharmagob.v1.repository_interfaces.dispatch_record import (
    DispatchRecordRepositoryInterface,
)

from ._base import BaseService


class DispatchRecordService(
    BaseService[DispatchRecordModel, DispatchRecordRepositoryInterface]
):
    __model__ = DispatchRecordModel

    def search_by_reference(
        self,
        reference_id: str,
        *,
        created_at_gt: int,
        created_at_lt: int,
        page: int,
        limit: int,
        umu_id: Optional[str] = None,
        dispatch_at_gt: Optional[int] = None,
        dispatch_at_lt: Optional[int] = None,
        service: Optional[str] = None,
    ) -> Tuple[int, Iterator[DispatchRecordModel]]:
        count, result = self.repository.search_by_reference(
            reference_id,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            page=page,
            limit=limit,
            umu_id=umu_id,
            dispatch_at_gt=dispatch_at_gt,
            dispatch_at_lt=dispatch_at_lt,
            service=service,
        )
        return count, map(lambda r: DispatchRecordModel(**r), result)
