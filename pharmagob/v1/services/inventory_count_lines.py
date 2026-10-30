from time import time
from typing import Any, Dict, Iterator, List, Optional, Tuple

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

    def search_by_item(
        self,
        search_str: str,
        *,
        umu_id: str,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        task_id: Optional[str] = None,
        status: Optional[List[str]] = None,
        lot: Optional[str] = None,
        is_in_system: Optional[bool] = None,
        adjustment_sign: Optional[str] = None,
        resolution_type: Optional[str] = None,
        resolution_origin: Optional[str] = None,
        resolved_at_gt: Optional[int] = None,
        resolved_at_lt: Optional[int] = None,
    ) -> Tuple[int, Iterator[InventoryCountLineModel]]:
        count, result = self.repository.search_by_item(
            search_str,
            umu_id=umu_id,
            task_id=task_id,
            status=status,
            lot=lot,
            is_in_system=is_in_system,
            adjustment_sign=adjustment_sign,
            resolution_type=resolution_type,
            resolution_origin=resolution_origin,
            resolved_at_gt=resolved_at_gt,
            resolved_at_lt=resolved_at_lt,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: InventoryCountLineModel(**r), result)
