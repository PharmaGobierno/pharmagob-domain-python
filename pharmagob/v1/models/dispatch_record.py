from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import UpdatableModel, uuid_by_params
from .minified import min_models, min_properties


class Status(str, Enum):
    DISPATCHED = "DISPATCHED"


class DispatchType(str, Enum):
    INHOSPITAL_DISPENSING = "INHOSPITAL_DISPENSING"
    PRESCRIPTION = "v"


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

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.reference_id)
