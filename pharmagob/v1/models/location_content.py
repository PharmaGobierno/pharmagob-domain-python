from dataclasses import dataclass

from ._base import BaseModel, UpdatableModel, uuid_by_params
from .minified import min_models


@dataclass(kw_only=True)
class LocationContentModel(BaseModel, UpdatableModel):
    __entity_name__ = "location-contents"

    umu_id: str
    quantity: int
    shipment_detail: min_models.ShipmentDetailMin
    item: min_models.ItemlMin
    location: min_models.LocationMin
    last_author: min_models.UserMin

    def __post_init__(self):
        self._id = uuid_by_params(
            self.shipment_detail.id, self.item.id, self.location.id
        )
