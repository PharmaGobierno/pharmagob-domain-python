from dataclasses import dataclass
from typing import Optional


@dataclass
class UserMin:
    id: str
    umu_id: str
    display_name: str


@dataclass
class ShipmentMin:
    id: str
    umu_id: str
    foreign_key: str
    order_id: str
    shipment_type: Optional[str] = None


@dataclass
class ShipmentDetailMin:
    id: str
    umu_id: str
    quantity: int
    shipment_id: str
    shipment_foreign_id: str
    shipment_order_id: str
    lot: str
    brand: Optional[str] = None


@dataclass
class ItemlMin:
    id: str
    foreign_id: str
    name: str


@dataclass
class LocationMin:
    id: str
    umu_id: str
    label_code: str
