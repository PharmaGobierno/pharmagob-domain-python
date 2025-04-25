from dataclasses import dataclass
from typing import List

from ._base import UpdatableModel, uuid_by_params
from .minified import min_models


@dataclass(kw_only=True)
class LocationContentModel(UpdatableModel):
    __entity_name__ = "location-contents"

    umu_id: str
    lot: str
    quantity: int
    item: min_models.ItemlMin
    location: min_models.LocationMin
    shipment_details: List[min_models.ShipmentDetailMin]
    last_author: min_models.UserMin

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.item.id, self.lot, self.location.id)
