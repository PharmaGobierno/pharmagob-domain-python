from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import BaseModel, uuid_by_params
from .minified import min_models


class ReviewStatus(str, Enum):
    NOT_EVALUATED = "NOT_EVALUATED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    PARTIAL_APPROVED = "PARTIAL_APPROVED"


class Status(str, Enum):
    DISPATCHED = "DISPATCHED"


class ShipmentType(str, Enum):
    URGENT = "URGENT"
    STANDARD = "STANDARD"  # ordinary
    LIFE_SUPPORT = "LIFE_SUPPORT"
    EXTRAORDINARY = "EXTRAORDINARY"


@dataclass(kw_only=True)
class ShipmentModel(BaseModel):
    __entity_name__ = "shipments"

    umu_id: str
    order_number: str
    load_id: str
    status: Status
    shipment_type: ShipmentType
    application_date: int
    user: min_models.UserMin
    order_id: Optional[str] = None
    review_status: ReviewStatus = ReviewStatus.NOT_EVALUATED

    def __post_init__(self):
        self._id = uuid_by_params(self.order_number, self.load_id)
