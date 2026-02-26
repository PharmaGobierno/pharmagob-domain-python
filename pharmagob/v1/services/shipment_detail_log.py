from pharmagob.v1.models.shipment_detail_log import ShipmentDetailLogModel
from pharmagob.v1.repository_interfaces.shipment_detail_log import (
    ShipmentDetailLogRepositoryInterface,
)

from ._base import BaseService


class ShipmentLogsService(
    BaseService[ShipmentDetailLogModel, ShipmentDetailLogRepositoryInterface]
):
    __model__ = ShipmentDetailLogModel
