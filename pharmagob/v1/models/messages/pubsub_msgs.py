from dataclasses import asdict, dataclass

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


@dataclass
class ShipmentStatusPubsubMessage(BasePubsubMessage):
    payload: ShipmentModel
