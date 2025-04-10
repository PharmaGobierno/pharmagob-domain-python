from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import BaseModel, uuid_by_params
from .minified import min_models


class States(str, Enum):
    INTEGRATED = "INTEGRATED"
    ACCEPTED = "ACCEPTED"
    DISPATCHED = "DISPATCHED"


@dataclass(kw_only=True)
class LocationContentStateModel(BaseModel):
    __entity_name__ = "location-content-states"

    umu_id: str
    location_content: min_models.LocationContentMin
    state: str
    transition_timestamp: int
    author: Optional[min_models.UserMin]
    context: Optional[dict]

    def __post_init__(self):
        self._id = uuid_by_params(self.location_content.id, self.transition_timestamp)
