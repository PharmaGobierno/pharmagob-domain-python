from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel, uuid_by_params


@dataclass(kw_only=True)
class DoctorModel(UpdatableModel):
    __entity_name__ = "doctors"

    umu_id: str
    name: str
    last_name_1: str
    last_name_2: Optional[str]
    employee_number: str
    profesional_licence: str
    specialty: Optional[str]
    service: list[str]
    level: Optional[str]
    status: str
    job_position: Optional[str]

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.employee_number, self.profesional_licence)
