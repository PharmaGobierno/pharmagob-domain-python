from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from ._base import UpdatableModel
from .minified import min_models
from .stock_transfer_event import Events


@dataclass(kw_only=True)
class StockTransferModel(UpdatableModel):
    __entity_name__ = "stock-transfers"

    umu_id: str
    reference_id: str = ""
    last_event: Events
    last_event_timestamp: int
    last_event_author: min_models.UserMin
    foreign_location_content: min_models.LocationContentMin
    created_quantity: int
    dispatched_quantity: Optional[int] = None
    received_quantity: Optional[int] = None
    location_content: Optional[min_models.LocationContentMin] = None
    context: Optional[dict] = None

    @classmethod
    def generate_reference_id(cls, uuid_str: str) -> str:
        """
        e.g. 550e8400e29b41d4a716446655440000
        """
        # UUID validation
        u = UUID(uuid_str)
        return f"{u.hex}"

    def __post_init__(self):
        super().__post_init__()
        if self.reference_id == "":
            self.reference_id = self.generate_reference_id(self._id)
