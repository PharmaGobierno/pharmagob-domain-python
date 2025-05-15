from dataclasses import dataclass
from typing import Optional


@dataclass
class DispatchDetailMin:
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
