from dataclasses import dataclass
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
class StockTransferEventModel(EventfulModel[Events]):
    __entity_name__ = "stock-transfer-events"

    umu_id: str
    stock_transfer_id: str
    stock_transfer_reference_id: str
    quantity: int
    author: min_models.UserMin
    foreign_location_content: min_models.LocationContentMin
    context: Optional[dict] = None

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.stock_transfer_id, self.transition_timestamp)
