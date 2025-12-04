from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel
from .minified.min_models import LocationMin


@dataclass(kw_only=True)
class LocationModel(UpdatableModel):
    __entity_name__ = "locations"

    umu_id: str
    label_code: Optional[str]
    verification_code: Optional[str]
    multiple_items: Optional[bool]
    is_global: bool
    disabled: bool = False

    def minified(self) -> LocationMin:
        return LocationMin(id=self._id, umu_id=self.umu_id, label_code=self.label_code)
