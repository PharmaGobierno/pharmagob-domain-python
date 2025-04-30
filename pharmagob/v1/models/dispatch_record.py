from dataclasses import dataclass
from enum import Enum

from typing import Optional
from ._base import UpdatableModel
from .minified import min_properties, min_models



class Status(str, Enum):
    DISPATCHED = "DISPATCHED"


class DispatchType(str, Enum):
    INHOSPITAL_DISPENSING = "INHOSPITAL_DISPENSING"
    PRESCRIPTION = "PRESCRIPTION"


@dataclass(kw_only=True)
class DispatchRecordModel(UpdatableModel):
    __entity_name__ = "dispatch-records"

    umu_id: str
    reference_id: str
    dispatch_type: DispatchType
    dispatch_at: int
    service: str
    status: Status = Status.DISPATCHED
    author: min_models.UserMin
    doctor: Optional[min_models.DoctorMin]
    patient: Optional[min_models.PatientMin]
    dispatch_details: list[min_properties.DispatchDetailMin]
