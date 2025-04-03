from dataclasses import dataclass

from pharmagob.v1.models.shipment import ShipmentModel


@dataclass
class BasePubsubMessage:
    payload: dict
    published_at: int
    author: dict
    version: str


@dataclass
class ShipmentStatusPubsubMessage(BasePubsubMessage):
    payload: ShipmentModel
