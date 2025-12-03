from pharmagob.v1.models.shipment_status import ShipmentStatusModel
from pharmagob.v1.repository_interfaces.shipment_logs import (
    ShipmentLogRepositoryInterface,
)

from ._base import BaseService


class ShipmentLogsService(
    BaseService[ShipmentStatusModel, ShipmentLogRepositoryInterface]
):
    __model__ = ShipmentStatusModel
