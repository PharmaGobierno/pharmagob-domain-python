from typing import Iterator, List, Optional, Tuple

from pharmagob.v1.models.shipment import ShipmentModel
from pharmagob.v1.repository_interfaces.shipments import ShipmentRepositoryInterface

from ._base import BaseService


class ShipmentService(BaseService[ShipmentModel, ShipmentRepositoryInterface]):
    __model__ = ShipmentModel

    def __init__(self, repository: ShipmentRepositoryInterface):
        super().__init__(repository)

    def paginated_query(
        self,
        conditions: List[tuple] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
    ) -> Tuple[int, Iterator[dict]]:
        count, query_result = self.repository.query_paginated(
            page=page, limit=limit, and_conditions=conditions, sort=sort
        )
        return count, query_result
