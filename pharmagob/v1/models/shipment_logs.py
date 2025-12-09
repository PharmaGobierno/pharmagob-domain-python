from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import BaseModel


@dataclass(kw_only=True)
class ShipmentLogModel(BaseModel):
    __entity_name__ = "shipment-logs"

    umu_id: str
    shipment: dict
    origin_timestamp: int
    origin: str
    context: Optional[dict] = None


# TODO: DEPRECATE
class StatusOrigins(str, Enum):
    BLUEYONDER = "BLUEYONDER"
    NOT_SPECIFIED = "NOT_SPECIFIED"
    MANUAL = "MANUAL"
