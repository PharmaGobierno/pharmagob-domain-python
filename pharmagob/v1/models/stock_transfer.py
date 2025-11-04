from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel
from .minified import min_models
from .stock_transfer_event import Events


@dataclass(kw_only=True)
class StockTransferModel(UpdatableModel):
    __entity_name__ = "stock-transfers"

    umu_id: str
    category: str
    reference_id: str = ""
    last_event: Events
    last_event_timestamp: int
    last_author: min_models.UserMin
    requested_quantity: int
    foreign_location_content: min_models.LocationContentMin
    foreign_dispatcher_author: Optional[min_models.UserMin] = None
    dispatched_quantity: Optional[int] = None
    accepted_quantity: Optional[int] = None
    context: Optional[dict] = None
