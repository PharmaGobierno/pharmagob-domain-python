from typing import Iterator, List, Optional, Tuple

from pharmagob.v1.models.shipment import ShipmentModel
from pharmagob.v1.repository_interfaces.shipments import ShipmentRepositoryInterface

from ._base import BaseService


class ShipmentService(BaseService[ShipmentModel, ShipmentRepositoryInterface]):
    __model__ = ShipmentModel

    def search_by_order_number(
        self,
        order_number: str,
        *,
        umu_id: str,
        page: int,
        limit: int,
        created_at_gt: Optional[int] = None,
        created_at_lt: Optional[int] = None,
        review_status_in: Optional[List[str]] = None
    ) -> Tuple[int, Iterator[ShipmentModel]]:
        count, result = self.repository.search_by_order_number(
            order_number,
            created_at_gt=created_at_gt,
            created_at_lt=created_at_lt,
            page=page,
            limit=limit,
            review_status=review_status_in,
            umu_id=umu_id,
        )
        return count, map(lambda r: ShipmentModel(**r), result)
