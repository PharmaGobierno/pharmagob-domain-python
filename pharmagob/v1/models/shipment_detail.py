from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel, uuid_by_params
from .minified import min_models


@dataclass(kw_only=True)
class ShipmentDetailModel(UpdatableModel):
    __entity_name__ = "shipment-details"

    umu_id: str
    shipment: min_models.ShipmentMin
    item: min_models.ItemMin
    lot: str
    expiration_date: int
    quantity: int
    last_author: Optional[min_models.UserMin]
    brand: Optional[str] = None
    accepted_quantity: Optional[int] = None

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.shipment.id, self.item.id, self.lot)
