from typing import Iterator, Tuple

from pharmagob.v1.models.dispatch_record_details import DispatchRecordDetailModel
from pharmagob.v1.repository_interfaces.dispatch_record_details import (
    DispatchRecordDetailRepositoryInterface,
)

from ._base import BaseService


class DispatchRecordDetailService(
    BaseService[DispatchRecordDetailModel, DispatchRecordDetailRepositoryInterface]
):
    __model__ = DispatchRecordDetailModel

    def get_by_dispatch_record_id(
        self, dispatch_record_id: str, *, umu_id: str, limit: int = 100000
    ) -> Tuple[int, Iterator[DispatchRecordDetailModel]]:
        count, result = self.repository.get_by_dispatch_record_id(
            dispatch_record_id, umu_id=umu_id, limit=limit
        )
        return count, map(lambda r: DispatchRecordDetailModel(**r), result)
