from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import UpdatableModel, uuid_by_params


class Status(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Specialty(str, Enum):
    CARDIOLOGY = "CARDIOLOGY"
    DERMATOLOGY = "DERMATOLOGY"
    GYNECOLOGY = "GYNECOLOGY"
    GENERAL_MEDICINE = "GENERAL_MEDICINE"
    NEUROLOGY = "NEUROLOGY"
    OPHTHALMOLOGY = "OPHTHALMOLOGY"
    ORTHOPEDICS = "ORTHOPEDICS"
    OTORHINOLARYNGOLOGY = "OTORHINOLARYNGOLOGY"
    PEDIATRICS = "PEDIATRICS"
    PSYCHIATRY = "PSYCHIATRY"
    UROLOGY = "UROLOGY"
    ANESTHESIOLOGY = "ANESTHESIOLOGY"
    DENTISTRY = "DENTISTRY"


class Services(str, Enum):
    SURGERY = "SURGERY"
    OUTPATIENT_CONSULTATION = "OUTPATIENT_CONSULTATION"
    HOSPITALIZATION = "HOSPITALIZATION"
    PREVENTIVE_MEDICINE = "PREVENTIVE_MEDICINE"
    REHABILITATION = "REHABILITATION"
    EMERGENCY_CARE = "EMERGENCY_CARE"
    LABORATORY = "LABORATORY"


class Level(str, Enum):
    JUNIOR = "JUNIOR"
    SPECIALIST = "SPECIALIST"
    RESIDENT = "RESIDENT"
    SENIOR = "SENIOR"


class Job_Position(str, Enum):
    RESIDENT = "RESIDENT"


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

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.employee_number, self.umu_id)
