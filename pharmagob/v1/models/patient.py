from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel, uuid_by_params


@dataclass(kw_only=True)
class PatientModel(UpdatableModel):
    __entity_name__ = "patients"

    umu_id: str
    name: str
    last_name_1: str
    last_name_2: Optional[str]
    curp: str
    phone_number: str
    email: Optional[str]
    birth: int
    postal_code: str
    state: str
    municipality: str
    neighborhood: Optional[str]
    country: Optional[str]

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.umu_id, self.curp)
