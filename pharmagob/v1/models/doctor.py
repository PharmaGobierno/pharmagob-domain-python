from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel, UpdatableModel


@dataclass(kw_only=True)
class DoctorModel(BaseModel, UpdatableModel):
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
