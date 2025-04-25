from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import UpdatableModel, uuid_by_params


class Status(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


@dataclass(kw_only=True)
class DoctorModel(UpdatableModel):
    __entity_name__ = "doctors"

    umu_id: str
    name: str
    last_name_1: str
    last_name_2: Optional[str] = None
    employee_number: str
    profesional_licence: str
    specialty: str
    service: list[str]
    status: Status
    level: Optional[str] = None
    job_position: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.employee_number, self.umu_id)
