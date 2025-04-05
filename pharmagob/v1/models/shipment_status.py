from dataclasses import dataclass

from ._base import BaseModel


@dataclass(kw_only=True)
class ShipmentStatusModel(BaseModel):
    __entity_name__ = "shipment-status"

    umu_id: str
    shipment_id: str
    status: str
    origin_timestamp: int
    origin: str
    context: dict
