from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel
from .minified import min_models


@dataclass(kw_only=True)
class ShipmentDetailLogModel(BaseModel):
    __entity_name__ = "shipment-detail-logs"

    umu_id: str
    shipment_detail: dict
    origin_timestamp: int
    origin: str
    author: Optional[min_models.UserMin] = None
    context: Optional[dict] = None
