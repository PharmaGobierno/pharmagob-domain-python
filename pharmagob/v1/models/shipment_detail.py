from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel, UpdatableModel
from .minified import min_models


@dataclass(kw_only=True)
class ShipmentDetailModel(BaseModel, UpdatableModel):
    __entity_name__ = "shipment-details"

    umu_id: str
    shipment: min_models.ShipmentMin
    item: min_models.ItemlMin
    lot: str
    quantity: int
    brand: Optional[str]
    last_author: Optional[min_models.UserMin]
