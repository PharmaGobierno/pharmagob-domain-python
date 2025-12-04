from dataclasses import dataclass, field
from typing import List, Optional

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
    location_content_ids: List[str] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.shipment.id, self.item.id, self.lot)

    def minified(self) -> min_models.ShipmentDetailMin:
        return min_models.ShipmentDetailMin(
            id=self._id,
            umu_id=self.umu_id,
            item_id=self.item.id,
            lot=self.lot,
            expiration_date=self.expiration_date,
            quantity=self.quantity,
            shipment_id=self.shipment.id,
            shipment_order_number=self.shipment.order_number,
            shipment_load_id=self.shipment.load_id,
            brand=self.brand,
        )
