from typing import Iterator, Optional, Tuple, List, Union

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
        page: int,
        limit: int,
        umu_id: Optional[str] = None,
        dispatch_at_gt: Optional[int] = None,
        dispatch_at_lt: Optional[int] = None,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
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
 
    
    def find_by_reference(
        self,
        reference_id: str,
        *,
        umu_id: Optional[str] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None,
        limit: Optional[int] = None,
    ) -> Tuple[int, Iterator[DispatchRecordModel]]:
        count, result = self.repository.find_by_reference(
            reference_id=reference_id,
            umu_id=umu_id,
            sort=sort,
            projection=projection,
            limit=limit,
        )

        return count, map(lambda r: DispatchRecordModel(**r), result)


    def exists_by_reference(
        self,
        reference_id: str,
        *,
        umu_id: str,
        exclude_statuses: Optional[List[str]] = None,
    ) -> bool:
        return self.repository.exists_by_reference(
            reference_id=reference_id,
            umu_id=umu_id,
            exclude_statuses=exclude_statuses,
        )
