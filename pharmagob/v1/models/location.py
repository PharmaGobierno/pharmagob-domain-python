from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel, UpdatableModel


@dataclass(kw_only=True)
class LocationModel(BaseModel, UpdatableModel):
    __entity_name__ = "locations"

    umu_id: str
    label_code: Optional[str]
    verification_code: Optional[str]
    multiple_items: Optional[bool]
    is_global: bool
    disabled: bool = False
