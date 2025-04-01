from dataclasses import dataclass

from .base.base import BaseModel
from .minified.user import UserMin


@dataclass(kw_only=True)
class ShipmentModel(BaseModel):
    __entity_name__ = "shipments"

    umu_id: str
    foreign_id: str
    order_id: str
    status: str
    shipment_type: str
    application_date: int
    user: UserMin
