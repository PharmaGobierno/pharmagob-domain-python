from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel
from .minified import min_models


@dataclass(kw_only=True)
class ShipmentDetailLogModel(BaseModel):
    __entity_name__ = "shipment-details-logs"

    umu_id: str
    shipment_id: str
    review_status: str
    origin_timestamp: int
    origin: str
    author: Optional[min_models.UserMin] = None
    context: Optional[dict] = None
