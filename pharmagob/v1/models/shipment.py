from dataclasses import dataclass
from enum import Enum

from ._base import BaseModel
from .minified import min_models


class ReviewStatus(str, Enum):
    NOT_EVALUATED = "NOT_EVALUATED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    PARTIAL_APPROVED = "PARTIAL_APPROVED"


class Status(str, Enum):
    DISPATCHED = "DISPATCHED"


@dataclass(kw_only=True)
class ShipmentModel(BaseModel):
    __entity_name__ = "shipments"

    umu_id: str
    foreign_id: str
    order_id: str
    status: str
    shipment_type: str
    application_date: int
    user: min_models.UserMin
    review_status: str = ReviewStatus.NOT_EVALUATED
