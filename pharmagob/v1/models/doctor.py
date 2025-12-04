from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import UpdatableModel, uuid_by_params
from .minified.min_models import DoctorMin


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
    status: Status = Status.ACTIVE
    level: Optional[str] = None
    job_position: Optional[str] = None

    full_name: Optional[str] = None

    def builder_full_name(self) -> str:
        return " ".join(filter(None, [self.name, self.last_name_1, self.last_name_2]))

    def update(self, data: dict):
        super().update(data)
        if data.get("name") or data.get("last_name_1") or data.get("last_name_2"):
            self.full_name = self.builder_full_name()

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.employee_number, self.umu_id)
        self.full_name = self.builder_full_name()

    def minified(self) -> DoctorMin:
        return DoctorMin(
            id=self._id,
            umu_id=self.umu_id,
            name=self.name,
            last_name_1=self.last_name_1,
            employee_number=self.employee_number,
            profesional_licence=self.profesional_licence,
            last_name_2=self.last_name_2,
        )
