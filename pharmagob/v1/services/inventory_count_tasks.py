from time import time
from typing import Dict, Iterator, List, Optional, Tuple

from pharmagob.v1.models.inventory_count_task import InventoryCountTaskModel, TaskStatus
from pharmagob.v1.repository_interfaces.inventory_count_tasks import (
    InventoryCountTaskRepositoryInterface,
)

from ._base import UmuScopedService


class InventoryCountTaskService(
    UmuScopedService[InventoryCountTaskModel, InventoryCountTaskRepositoryInterface]
):
    __model__ = InventoryCountTaskModel

    def claim(
        self,
        entity_id: str,
        *,
        expected_statuses: List[TaskStatus],
        data: dict,
        umu_id: str,
    ) -> Optional[InventoryCountTaskModel]:
        result = self.repository.claim(
            entity_id,
            expected_statuses=expected_statuses,
            data={**data, "updated_at": round(time() * 1000)},
            umu_id=umu_id,
        )
        if not result:
            return None
        return InventoryCountTaskModel(**result)

    def increment(
        self,
        entity_id: str,
        *,
        quantities: Dict[str, int],
        umu_id: str,
    ) -> int:
        return self.repository.increment(
            entity_id, quantities=quantities, umu_id=umu_id
        )

    def search_by_task_name(
        self,
        search_str: str,
        *,
        umu_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        count_type: Optional[str] = None,
        status: Optional[List[str]] = None,
        cyclic_mode: Optional[str] = None,
        scheduled_at_gt: Optional[int] = None,
        scheduled_at_lt: Optional[int] = None,
    ) -> Tuple[int, Iterator[InventoryCountTaskModel]]:
        count, result = self.repository.search_by_task_name(
            search_str,
            umu_id=umu_id,
            count_type=count_type,
            status=status,
            cyclic_mode=cyclic_mode,
            scheduled_at_gt=scheduled_at_gt,
            scheduled_at_lt=scheduled_at_lt,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: InventoryCountTaskModel(**r), result)

    def search_by_reference_id(
        self,
        search_str: str,
        *,
        umu_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        count_type: Optional[str] = None,
        status: Optional[List[str]] = None,
        cyclic_mode: Optional[str] = None,
        scheduled_at_gt: Optional[int] = None,
        scheduled_at_lt: Optional[int] = None,
    ) -> Tuple[int, Iterator[InventoryCountTaskModel]]:
        count, result = self.repository.search_by_reference_id(
            search_str,
            umu_id=umu_id,
            count_type=count_type,
            status=status,
            cyclic_mode=cyclic_mode,
            scheduled_at_gt=scheduled_at_gt,
            scheduled_at_lt=scheduled_at_lt,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: InventoryCountTaskModel(**r), result)
