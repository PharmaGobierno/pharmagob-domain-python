from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import UpdatableModel, uuid_by_params
from .minified import min_models


class ReviewStatus(str, Enum):
    NOT_EVALUATED = "NOT_EVALUATED"
    REJECTED = "REJECTED"
    APPROVED = "APPROVED"
    PARTIAL_APPROVED = "PARTIAL_APPROVED"
    IN_PROGRESS = "IN_PROGRESS"


class Status(str, Enum):
    DISPATCHED = "DISPATCHED"


class ShipmentType(str, Enum):
    STANDARD = "STANDARD"  # manual
    ISEMEMB = "ISEMEMB"
    ORD = "ORD"  # ordinary
    RTS = "RTS"  # rutas de salud
    SPV = "SPV"  # soporte de vida
    URG = "URG"  # urgente
    FARB = "FARB"  # farmacias del bienestar


@dataclass(kw_only=True)
class ShipmentModel(UpdatableModel):
    __entity_name__ = "shipments"

    umu_id: str
    order_number: str
    load_id: str
    status: Status
    shipment_type: str
    application_date: int
    user: min_models.UserMin
    order_id: Optional[str] = None
    review_status: ReviewStatus = ReviewStatus.NOT_EVALUATED

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.order_number, self.load_id)

    def minified(self) -> min_models.ShipmentMin:
        return min_models.ShipmentMin(
            id=self._id,
            umu_id=self.umu_id,
            order_number=self.order_number,
            load_id=self.load_id,
            shipment_type=self.shipment_type,
            order_id=self.order_id,
        )
