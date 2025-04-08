from dataclasses import dataclass

from ._base import BaseModel
from .minified import min_models


@dataclass(kw_only=True)
class ShipmentStatusModel(BaseModel):
    __entity_name__ = "shipment-status"

    umu_id: str
    shipment: min_models.ShipmentMin
    status: str
    origin_timestamp: int
    origin: str
    context: dict
