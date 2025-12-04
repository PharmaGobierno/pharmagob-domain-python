from dataclasses import dataclass
from typing import List, Optional

from ._base import UpdatableModel, uuid_by_params
from .minified import min_models


@dataclass(kw_only=True)
class LocationContentModel(UpdatableModel):
    __entity_name__ = "location-contents"

    umu_id: str
    lot: str
    expiration_date: int
    quantity: int
    item: min_models.ItemMin
    location: min_models.LocationMin
    shipment_details: Optional[List[min_models.ShipmentDetailMin]] = None
    last_author: min_models.UserMin

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.item.id, self.lot, self.location.id)

    def minified(self) -> min_models.LocationContentMin:
        return min_models.LocationContentMin(
            id=self._id,
            umu_id=self.umu_id,
            item_id=self.item.id,
            lot=self.lot,
            expiration_date=self.expiration_date,
            location_id=self.location.id,
            quantity=self.quantity,
        )
