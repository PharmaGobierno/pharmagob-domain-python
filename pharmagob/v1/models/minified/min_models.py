from dataclasses import dataclass
from typing import Optional

from pharmagob.v1.models._base import DictModelMixin


@dataclass
class UserMin(DictModelMixin):
    id: str
    umu_id: str
    display_name: str


@dataclass
class ShipmentMin(DictModelMixin):
    id: str
    umu_id: str
    order_number: str
    load_id: str
    order_id: Optional[str] = None
    shipment_type: Optional[str] = None


@dataclass
class ShipmentDetailMin(DictModelMixin):
    id: str
    umu_id: str
    item_id: str
    lot: str
    quantity: int
    shipment_id: str
    shipment_order_number: str
    shipment_load_id: str
    brand: Optional[str]


@dataclass
class ItemlMin(DictModelMixin):
    id: str
    foreign_id: str
    name: str


@dataclass
class LocationMin(DictModelMixin):
    id: str
    umu_id: str
    label_code: Optional[str]


@dataclass
class LocationContentMin(DictModelMixin):
    id: str
    umu_id: str
    item_id: str
    lot: str
    location_id: str
    quantity: int
