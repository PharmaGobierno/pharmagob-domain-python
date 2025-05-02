from dataclasses import dataclass
from typing import Optional


@dataclass
class UserMin:
    id: str
    umu_id: str
    display_name: str


@dataclass
class DoctorMin:
    id: str
    umu_id: str
    name: str
    last_name_1: str
    last_name_2: Optional[str]
    employee_number: str
    profesional_licence: str


@dataclass
class PatientMin:
    id: str
    umu_id: str
    name: str
    last_name_1: str
    last_name_2: Optional[str]
    curp: str
    birth: int
    email: Optional[str]


@dataclass
class ShipmentMin:
    id: str
    umu_id: str
    order_number: str
    load_id: str
    shipment_type: str
    order_id: Optional[str] = None


@dataclass
class ShipmentDetailMin:
    id: str
    umu_id: str
    item_id: str
    lot: str
    expiration_date: int
    quantity: int
    shipment_id: str
    shipment_order_number: str
    shipment_load_id: str
    brand: Optional[str] = None


@dataclass
class ItemlMin:
    id: str
    foreign_id: str
    description: Optional[str] = None  # TODO: required
    short_description: Optional[str] = None  # TODO: required


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
    expiration_date: int
    location_id: str
    quantity: int


@dataclass
class DispatchRecordMin:
    id: str
    umu_id: str
    reference_id: str
    dispatch_type: str
    dispatch_at: int
    doctor_id: Optional[str]
    patient_id: Optional[str]
