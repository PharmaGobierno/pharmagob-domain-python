from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ._base import UpdatableModel, uuid_by_params
from .minified import min_models


class Status(str, Enum):
    DISPATCHED = "DISPATCHED"
    PARTIAL_DISPATCHED = "PARTIAL_DISPATCHED"


class Services(str, Enum):
    SURGERY = "SURGERY"
    OUTPATIENT_CONSULTATION = "OUTPATIENT_CONSULTATION"
    HOSPITALIZATION = "HOSPITALIZATION"
    PREVENTIVE_MEDICINE = "PREVENTIVE_MEDICINE"
    REHABILITATION = "REHABILITATION"
    EMERGENCY_CARE = "EMERGENCY_CARE"
    LABORATORY = "LABORATORY"


class DispatchType(str, Enum):
    INHOSPITAL_DISPENSING = "INHOSPITAL_DISPENSING"
    PRESCRIPTION = "PRESCRIPTION"


class DispatchCategory(str, Enum):
    MEDICATION = "MEDICATION"
    MEDICAL_SUPPLIES = "MEDICAL_SUPPLIES"
    MIXED = "MIXED"


@dataclass(kw_only=True)
class DispatchRecordModel(UpdatableModel):
    __entity_name__ = "dispatch-records"

    umu_id: str
    category: str
    reference_id: str
    dispatch_type: str
    dispatch_at: int
    service: str
    status: Status
    author: min_models.UserMin
    dispatch_details: Optional[List[min_models.DispatchRecordDetailMin]] = None
    dispatch_notes: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.reference_id, self.umu_id)
