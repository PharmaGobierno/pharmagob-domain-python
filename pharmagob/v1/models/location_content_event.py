from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import BaseModel, uuid_by_params
from .minified import min_models


class Events(str, Enum):
    INTEGRATED = "INTEGRATED"
    ACCEPTED = "ACCEPTED"
    DISPATCHED = "DISPATCHED"


@dataclass(kw_only=True)
class LocationContentEventModel(BaseModel):
    __entity_name__ = "location-content-events"

    umu_id: str
    location_content: min_models.LocationContentMin
    event: Events
    transition_timestamp: int
    author: Optional[min_models.UserMin]
    context: Optional[dict]

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.location_content.id, self.transition_timestamp)
