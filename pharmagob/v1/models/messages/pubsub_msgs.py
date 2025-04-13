from dataclasses import asdict, dataclass
from typing import Any, Optional

from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.models.minified import min_models
from pharmagob.v1.models.shipment import ShipmentModel


@dataclass
class BasePubsubMessage:
    payload: Any
    origin_timestamp: int
    published_at: int
    author: min_models.UserMin
    context: Optional[dict]
    version: str

    def dict(self):
        return asdict(self)

    @classmethod
    def topic(cls) -> str:
        raise NotImplementedError


@dataclass(kw_only=True)
class ShipmentStatusPubsubMessage(BasePubsubMessage):
    payload: ShipmentModel
    status: str
    origin: Optional[str] = None
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "shipment-status"


@dataclass(kw_only=True)
class LocationContentEventsPubsubMessage(BasePubsubMessage):
    payload: LocationContentModel
    event: str
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "location-content-events"
