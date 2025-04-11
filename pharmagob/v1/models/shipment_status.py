from dataclasses import dataclass
from enum import Enum

from ._base import BaseModel
from .minified import min_models


class StatusOrigins(str, Enum):
    BLUYONDER = "BLUEYONDER"
    NOT_SPECIFIED = "NOT_SPECIFIED"


@dataclass(kw_only=True)
class ShipmentStatusModel(BaseModel):
    __entity_name__ = "shipment-status"

    umu_id: str
    shipment: min_models.ShipmentMin
    status: StatusOrigins
    origin_timestamp: int
    origin: str
    context: dict
