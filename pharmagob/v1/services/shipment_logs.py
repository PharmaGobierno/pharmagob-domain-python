from pharmagob.v1.models.shipment_logs import ShipmentLogModel
from pharmagob.v1.repository_interfaces.shipment_logs import (
    ShipmentLogRepositoryInterface,
)

from ._base import BaseService


class ShipmentLogsService(
    BaseService[ShipmentLogModel, ShipmentLogRepositoryInterface]
):
    __model__ = ShipmentLogModel
