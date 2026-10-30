from dataclasses import dataclass
from typing import List, Optional


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
    employee_number: str
    profesional_licence: str
    last_name_2: Optional[str] = None


@dataclass
class PatientMin:
    id: str
    umu_id: str
    name: str
    last_name_1: str
    curp: str
    birth: int
    email: Optional[str] = None
    last_name_2: Optional[str] = None


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
class ItemMin:
    id: str
    foreign_id: str
    description: str
    is_controlled: bool
    category: str
    sub_category: str
    short_description: Optional[str] = None


@dataclass
class LocationMin:
    id: str
    umu_id: str
    label_code: Optional[str] = None


@dataclass
class LocationContentMin:
    id: str
    umu_id: str
    item_id: str
    lot: str
    expiration_date: int
    location_id: str
    quantity: int
    label_code: Optional[str] = None



@dataclass
class DispatchRecordMin:
    id: str
    umu_id: str
    reference_id: str
    dispatch_type: str
    dispatch_at: int
    service: str
    category: str
    prescribed_at: Optional[int] = None


@dataclass
class DispatchRecordDetailMin:
    id: str
    umu_id: str
    dispatch_record_id: str
    dispatch_record_reference_id: str
    item_id: str
    quantity: int
    dispatch_at: int
    location_content_id: str
    doctor_id: Optional[str] = None
    patient_id: Optional[str] = None
    prescribed_quantity: Optional[int] = None
    prescribed_at: Optional[int] = None
    context: Optional[dict] = None

@dataclass
class ReportRequestMin:
    id: str
    status: str
    report_type: str
    progress: int
    user_id: str


@dataclass
class CountTaskMin:
    id: str
    reference_id: str
    task_name: str
    count_type: str


@dataclass
class CountScheduleMin:
    id: str
    schedule_name: str
    frequency: str


@dataclass
class CountLineMin:
    id: str
    item_id: str
    lot: str
    location_id: str
    status: str


@dataclass
class CountEntryMin:
    round: int
    counted_quantity: int
    kardex_snapshot_quantity: int  # location-content quantity when this round was captured
    author: UserMin
    counted_at: int

    def __post_init__(self):
        if isinstance(self.author, dict):
            self.author = UserMin(**self.author)


@dataclass
class CountItemFilterMin:
    item_ids: Optional[List[str]] = None
    families: Optional[List[str]] = None  # phase 2
    is_high_cost: Optional[bool] = None  # phase 2


@dataclass
class CountRuleMin:
    case: int
    note: str


@dataclass
class CountResolutionMin:
    type: str
    origin: str
    author: UserMin
    resolved_at: int
    adjustment_quantity: int  # signed, 0 on rejection and no difference
    final_quantity: int

    def __post_init__(self):
        if isinstance(self.author, dict):
            self.author = UserMin(**self.author)


@dataclass
class CountLinesQuantitiesMin:
    total_quantity: int = 0
    counted_quantity: int = 0
    resolved_quantity: int = 0
