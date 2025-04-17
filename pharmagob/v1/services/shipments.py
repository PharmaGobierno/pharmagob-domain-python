from typing import List, Optional, Tuple

from pharmagob.v1.models.shipment import ShipmentModel
from pharmagob.v1.repository_interfaces.shipments import ShipmentRepositoryInterface

from ._base import BaseService


class ShipmentService(BaseService[ShipmentModel, ShipmentRepositoryInterface]):
    __model__ = ShipmentModel

    def sarch_by_order_number(
        self,
        order_number: str,
        *,
        created_at_gt: int,
        created_at_lt: int,
        page: int,
        limit: int,
        review_status: Optional[str] = None
    ) -> Tuple[int, List[ShipmentModel]]:
        count, result = self.repository.sarch_by_order_number(
            order_number,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            page=page,
            limit=limit,
            review_status=review_status,
        )
        return count, [ShipmentModel(**r) for r in result]
