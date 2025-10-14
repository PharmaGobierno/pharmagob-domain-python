from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import UpdatableModel
from .minified import min_models


class AdministrationType(str, Enum):
    ORAL = "ORAL"
    INTRAVENOUS = "INTRAVENOUS"
    TOPICAL = "TOPICAL"
    INHALATION = "INHALATION"
    SUBCUTANEOUS = "SUBCUTANEOUS"


@dataclass(kw_only=True)
class DispatchRecordDetailModel(UpdatableModel):
    __entity_name__ = "dispatch-record-details"

    umu_id: str
    dispatch_record: min_models.DispatchRecordMin
    dispatch_at: int
    author: min_models.UserMin
    quantity: int
    prescribed_quantity: Optional[int] = None
    location_content: min_models.LocationContentMin
    item: min_models.ItemMin
    administration_type: Optional[str] = None
    doctor: Optional[min_models.DoctorMin] = None
    patient: Optional[min_models.PatientMin] = None
    patient_bed: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.prescribed_quantity is None:
            self.prescribed_quantity = self.quantity
