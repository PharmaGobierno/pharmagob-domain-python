from typing import Iterator, Tuple

from pharmagob.v1.models.shipment_detail import ShipmentDetailModel
from pharmagob.v1.repository_interfaces.shipment_details import (
    ShipmentDetailRepositoryInterface,
)

from ._base import BaseService


class ShipmentDetailService(
    BaseService[ShipmentDetailModel, ShipmentDetailRepositoryInterface]
):
    __model__ = ShipmentDetailModel

    def get_by_shipment_id(
        self, shipment_id: str, *, umu_id: str
    ) -> Tuple[int, Iterator[ShipmentDetailModel]]:
        count, result = self.repository.get_by_shipment_id(shipment_id, umu_id=umu_id)
        return count, map(lambda r: ShipmentDetailModel(**r), result)
