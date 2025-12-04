from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel, uuid_by_params
from .minified.min_models import PatientMin


@dataclass(kw_only=True)
class PatientModel(UpdatableModel):
    __entity_name__ = "patients"

    umu_id: str
    name: str
    last_name_1: str
    last_name_2: Optional[str] = None
    curp: str
    is_real_curp: bool = True
    phone_number: str
    email: Optional[str]
    birth: int
    postal_code: Optional[str] = None
    state: Optional[str] = None
    municipality: Optional[str] = None
    neighborhood: Optional[str] = None
    country: Optional[str] = None
    street_address: Optional[str] = None

    full_name: Optional[str] = None

    def builder_full_name(self) -> str:
        return " ".join(filter(None, [self.name, self.last_name_1, self.last_name_2]))

    def update(self, data: dict):
        super().update(data)
        if data.get("name") or data.get("last_name_1") or data.get("last_name_2"):
            self.full_name = self.builder_full_name()

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.umu_id, self.curp)
        self.full_name = self.builder_full_name()

    def minified(self) -> PatientMin:
        return PatientMin(
            id=self._id,
            umu_id=self.umu_id,
            name=self.name,
            last_name_1=self.last_name_1,
            last_name_2=self.last_name_2,
            curp=self.curp,
            birth=self.birth,
            email=self.email,
        )
