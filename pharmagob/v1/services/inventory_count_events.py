from typing import Dict, Iterator, List, Optional, Tuple

from pharmagob.v1.models.inventory_count_event import InventoryCountEventModel
from pharmagob.v1.repository_interfaces.inventory_count_events import (
    InventoryCountEventRepositoryInterface,
)

from ._base import UmuScopedService


class InventoryCountEventService(
    UmuScopedService[InventoryCountEventModel, InventoryCountEventRepositoryInterface]
):
    __model__ = InventoryCountEventModel

    def search_by_reference_id(
        self,
        search_str: str,
        *,
        umu_id: str,
        created_at_gt: int,
        created_at_lt: int,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[Dict[str, int]] = None,
        event: Optional[List[str]] = None,
        author_id: Optional[str] = None,
    ) -> Tuple[int, Iterator[InventoryCountEventModel]]:
        count, result = self.repository.search_by_reference_id(
            search_str,
            umu_id=umu_id,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            event=event,
            author_id=author_id,
            page=page,
            limit=limit,
            sort=sort,
        )
        return count, map(lambda r: InventoryCountEventModel(**r), result)
