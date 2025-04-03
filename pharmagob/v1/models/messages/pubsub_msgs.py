from dataclasses import asdict, dataclass

from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.models.minified import min_models
from pharmagob.v1.models.shipment import ShipmentModel


@dataclass
class BasePubsubMessage:
    payload: dict
    published_at: int
    author: min_models.UserMin
    version: str

    def dict(self):
        return asdict(self)

    @classmethod
    def topic(cls) -> str:
        raise NotImplementedError


@dataclass
class ShipmentStatusPubsubMessage(BasePubsubMessage):
    payload: ShipmentModel
    status: str
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "shipment-status"


@dataclass
class LocationContentStatesPubsubMessage(BasePubsubMessage):
    payload: LocationContentModel
    state: str
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "location-content-states"
