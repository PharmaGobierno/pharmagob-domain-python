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

    def __init__(self, repository: ShipmentDetailRepositoryInterface):
        super().__init__(repository)

    def get_by_shipment_id(self, shipment_id: str) -> Tuple[int, Iterator[dict]]:
        return self.repository.get_by_shipment_id(shipment_id)
