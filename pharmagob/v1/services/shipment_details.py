from pharmagob.v1.models.shipment_detail import ShipmentDetailModel
from pharmagob.v1.repository_interfaces.shipment_details import (
    ShipmentDetailRepositoryInterface,
)

from ._base import BaseService


class ShipmentDetailService(
    BaseService[ShipmentDetailModel, ShipmentDetailRepositoryInterface]
):
    def get_by_shipment_id(self, shipment_id: str) -> list[ShipmentDetailModel]: ...

    pass
