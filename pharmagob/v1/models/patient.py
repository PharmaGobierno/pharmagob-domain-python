from dataclasses import dataclass, field
from typing import Optional

from ._base import UpdatableModel, uuid_by_params


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

    full_name: str = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.umu_id, self.curp)
        self.full_name = (
            f"{self.name} {self.last_name_1} {self.last_name_2 or ''}".strip()
        )
