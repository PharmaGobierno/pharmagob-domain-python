from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel, uuid_by_params
from .minified import min_models


@dataclass(kw_only=True)
class LocationContentStateModel(BaseModel):
    __entity_name__ = "location-content-states"

    umu_id: str
    location_content_id: str
    state: str
    transition_timestamp: int
    author: Optional[min_models.UserMin]
    context: Optional[dict]

    def __post_init__(self):
        self._id = uuid_by_params(self.location_content_id, self.transition_timestamp)
