from pharmagob.v1.models.shipment_detail import ShipmentDetailModel
from pharmagob.v1.repository_interfaces.shipment_details import (
    ShipmentDetailRepositoryInterface,
)

from ._base import BaseService


class ShipmentDetailService(
    BaseService[ShipmentDetailModel, ShipmentDetailRepositoryInterface]
):

    pass
