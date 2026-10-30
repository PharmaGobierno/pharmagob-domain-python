from time import time
from typing import Any, List, Optional, Tuple

from pharmagob.v1.models.inventory_count_line import InventoryCountLineModel, LineStatus
from pharmagob.v1.repository_interfaces.inventory_count_lines import (
    InventoryCountLineRepositoryInterface,
)

from ._base import UmuScopedService


class InventoryCountLineService(
    UmuScopedService[InventoryCountLineModel, InventoryCountLineRepositoryInterface]
):
    __model__ = InventoryCountLineModel

    def claim(
        self,
        entity_id: str,
        *,
        expected_statuses: List[LineStatus],
        data: dict,
        umu_id: str,
    ) -> Optional[InventoryCountLineModel]:
        result = self.repository.claim(
            entity_id,
            expected_statuses=expected_statuses,
            data={**data, "updated_at": round(time() * 1000)},
            umu_id=umu_id,
        )
        if not result:
            return None
        return InventoryCountLineModel(**result)

    def insert_many_ignore_duplicates(
        self, entities: List[InventoryCountLineModel]
    ) -> Tuple[int, int, int]:
        """Returns (inserted, duplicated, locked), see the repository port."""
        return self.repository.insert_many_ignore_duplicates(
            [entity.dict() for entity in entities]
        )

    def soft_delete_by_task(
        self,
        task_id: str,
        *,
        umu_id: str,
        deleted_at: Optional[int] = None,
    ) -> int:
        return self.repository.soft_delete_by_task(
            task_id,
            deleted_at=deleted_at or round(time() * 1000),
            umu_id=umu_id,
        )

    def delete_many(
        self,
        and_conditions: Optional[List[Tuple[str, str, Any]]],
        *,
        limit: Optional[int] = None,
    ) -> int:
        return self.repository.delete_many(and_conditions, limit=limit)
