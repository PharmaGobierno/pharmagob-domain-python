from time import time
from typing import Dict, List, Optional

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
