from dataclasses import dataclass


@dataclass
class UserMin:
    id: str
    umu_id: str
    display_name: str


@dataclass
class ShipmentDetailMin:
    id: str
    umu_id: str
    lot: str
    brand: str


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
