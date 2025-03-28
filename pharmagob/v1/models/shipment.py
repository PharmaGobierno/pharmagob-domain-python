from enum import Enum

from .base.base import BaseModel
from .minified.user import UserMin


class ShipmentModel(BaseModel):
    __entity_name__ = "shipments"

    umu_id: str
    foreign_id: str
    order_id: str
    status: Enum
    shipment_type: Enum
    application_date: int
    user: UserMin
