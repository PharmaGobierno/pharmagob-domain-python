from dataclasses import dataclass

from ._base import BaseModel, UpdatableModel
from .minified import min_models


@dataclass(kw_only=True)
class LocationContentModel(BaseModel, UpdatableModel):
    __entity_name__ = "location-contents"

    umu_id: str
    quantity: int
    shipment_detail: min_models.ShipmentDetailMin
    user: min_models.UserMin
    item: min_models.ItemlMin
