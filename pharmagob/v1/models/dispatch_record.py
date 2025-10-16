from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ._base import UpdatableModel
from .minified import min_models


class Status(str, Enum):
    DISPATCHED = "DISPATCHED"
    PARTIAL_DISPATCHED = "PARTIAL_DISPATCHED"
    CANCELLED = "CANCELLED"


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
    prescribed_at: Optional[int] = None
