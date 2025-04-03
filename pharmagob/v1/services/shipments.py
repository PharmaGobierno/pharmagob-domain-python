from pharmagob.v1.models.shipment import ShipmentModel
from pharmagob.v1.repository_interfaces.shipments import ShipmentRepositoryInterface

from ._base import BaseService


class ShipmentService(BaseService[ShipmentModel, ShipmentRepositoryInterface]):

    pass
