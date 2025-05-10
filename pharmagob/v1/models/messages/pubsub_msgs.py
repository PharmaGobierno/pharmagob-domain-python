from dataclasses import asdict, dataclass
from time import time
from typing import Any, Dict, Optional

from pharmagob.v1.models.dispatch_record import DispatchRecordModel
from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.models.minified import min_models
from pharmagob.v1.models.shipment import ShipmentModel
from pharmagob.v1.models.shipment_detail import ShipmentDetailModel


@dataclass
class BasePubsubMessage:
    payload: Any
    origin_timestamp: int
    author: min_models.UserMin
    version: str
    published_at: int = round(time() * 1000)
    context: Optional[dict] = None

    def dict(self):
        return asdict(self)

    @classmethod
    def topic(cls) -> str:
        raise NotImplementedError

    def get_attributes(self) -> Dict[str, str]:
        return {"topic": self.topic(), "version": self.version}


@dataclass(kw_only=True)
class ShipmentStatusPubsubMessage(BasePubsubMessage):
    payload: ShipmentModel
    status: str
    origin: str
    items: Optional[list[dict]] = None
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "shipment-status"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {**default_attributes, "origin": self.origin, "status": self.status}


@dataclass(kw_only=True)
class LocationContentEventsPubsubMessage(BasePubsubMessage):
    payload: LocationContentModel
    event: str
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "location-content-events"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {**default_attributes, "event": self.event}


@dataclass(kw_only=True)
class ValidationShipmentDetailsPubsubMessage(BasePubsubMessage):
    payload: ShipmentDetailModel
    accepted_item_quantity: int
    status: str
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "shipment-detail-validations"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {**default_attributes, "status": self.status}


@dataclass(kw_only=True)
class ShipmentIntegrationsPubsubMessage(BasePubsubMessage):
    payload: dict
    origin: str
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "shipment-integrations"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {**default_attributes, "origin": self.origin}


@dataclass(kw_only=True)
class DispatchRecordsPubsubMessage(BasePubsubMessage):
    payload: DispatchRecordModel
    status: str
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "dispatch-records"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {**default_attributes, "status": self.status}
