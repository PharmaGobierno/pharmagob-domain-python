from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import BaseModel, uuid_by_params
from .minified import min_models


class QuantityEvents(str, Enum):
    INCREASE = "INCREASE"
    SUBSTRACT = "SUBSTRACT"


@dataclass(kw_only=True)
class LocationContentQuantityLogModel(BaseModel):
    __entity_name__ = "location-content-quantity-logs"

    umu_id: str
    location_content: min_models.LocationContentMin
    quantity_event: QuantityEvents
    origin_timestamp: int
    author: Optional[min_models.UserMin]
    context: Optional[dict]

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(
            self.location_content.id, self.quantity_event, self.origin_timestamp
        )
