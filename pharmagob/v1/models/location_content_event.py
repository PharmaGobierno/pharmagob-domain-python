from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import EventfulModel, uuid_by_params
from .minified import min_models


class Events(str, Enum):
    INTEGRATED = "INTEGRATED"
    ACCEPTED = "ACCEPTED"
    DISPATCHED = "DISPATCHED"
    ISSUE_RECORD_ACCEPTED = "ISSUE_RECORD_ACCEPTED"
    ISSUE_RECORD_DISPATCHED = "ISSUE_RECORD_DISPATCHED"


@dataclass(kw_only=True)
class LocationContentEventModel(EventfulModel[Events]):
    __entity_name__ = "location-content-events"

    umu_id: str
    location_content: min_models.LocationContentMin
    author: Optional[min_models.UserMin]
    context: Optional[dict]

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.location_content.id, self.transition_timestamp)
