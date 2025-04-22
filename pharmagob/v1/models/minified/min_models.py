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
    item_id: str
    lot: str
    quantity: int
    shipment_id: str
    shipment_order_number: str
    shipment_load_id: str
    brand: Optional[str]


@dataclass
class ItemlMin:
    id: str
    foreign_id: str
    name: str


@dataclass
class LocationMin:
    id: str
    umu_id: str
    label_code: Optional[str]


@dataclass
class LocationContentMin:
    id: str
    umu_id: str
    item_id: str
    lot: str
    location_id: str
    quantity: int


@dataclass
class DispatchRecordMin:
    id: str
    umu_id: str
    reference_id: str
    dispatch_type: str
    dispatch_date: int
    doctor_id: Optional[str]
    patien_id: Optional[str]
