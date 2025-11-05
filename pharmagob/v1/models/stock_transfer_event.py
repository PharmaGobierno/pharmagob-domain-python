from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ._base import EventfulModel, uuid_by_params
from .minified import min_models


class Events(str, Enum):
    CREATED = "CREATED"
    DISPATCHED = "DISPATCHED"
    RECEIVED = "RECEIVED"
    CLOSED = "CLOSED"


@dataclass(kw_only=True)
class StockTransferEventContext:
    requested_quantity: Optional[int] = None
    accepted_quantity: Optional[int] = None
    dispatched_quantity: Optional[int] = None
    notes: Optional[str] = None


@dataclass(kw_only=True)
class StockTransferEventModel(EventfulModel[Events]):
    __entity_name__ = "stock-transfer-events"

    umu_id: str
    category: str
    stock_transfer_id: str
    stock_transfer_reference_id: str
    author: min_models.UserMin
    foreign_location_content: min_models.LocationContentMin
    context: StockTransferEventContext = field(
        default_factory=StockTransferEventContext
    )

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.stock_transfer_id, self.transition_timestamp)
