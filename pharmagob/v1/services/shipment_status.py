from pharmagob.v1.models.shipment_status import ShipmentStatusModel
from pharmagob.v1.repository_interfaces.shipment_status import (
    ShipmentStatusRepositoryInterface,
)

from ._base import BaseService


class ShipmentStatusService(
    BaseService[ShipmentStatusModel, ShipmentStatusRepositoryInterface]
):
    __model__ = ShipmentStatusModel
