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
    order_number: str
    load_id: str
    order_id: Optional[str] = None
    shipment_type: Optional[str] = None


@dataclass
class ShipmentDetailMin:
    id: str
    umu_id: str
    quantity: int
    shipment_id: str
    shipment_order_number: str
    shipment_load_id: str
    lot: str
    shipment_order_id: Optional[str] = None
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
