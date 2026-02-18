from dataclasses import asdict, dataclass, field
from time import time
from typing import Any, Dict, Optional

from pharmagob.v1.models.dispatch_record import DispatchRecordModel
from pharmagob.v1.models.dispatch_record_details import DispatchRecordDetailModel
from pharmagob.v1.models.item import ItemModel
from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.models.minified import min_models
from pharmagob.v1.models.shipment import ShipmentModel
from pharmagob.v1.models.shipment_detail import ShipmentDetailModel
from pharmagob.v1.models.stock_transfer import StockTransferModel


@dataclass
class BasePubsubMessage:
    payload: Any
    origin_timestamp: int
    author: min_models.UserMin
    version: str
    published_at: int = field(default_factory=lambda: round(time() * 1000))
    context: Optional[dict] = None

    def dict(self):
        return asdict(self)

    @classmethod
    def topic(cls) -> str:
        raise NotImplementedError

    def get_attributes(self) -> Dict[str, str]:
        return {"topic": self.topic(), "version": self.version}


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


@dataclass(kw_only=True)
class DispatchRecordDetailsPubsubMessage(BasePubsubMessage):
    payload: DispatchRecordDetailModel
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "dispatch-record-details"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return default_attributes


@dataclass(kw_only=True)
class StockTransferEventsPubsubMessage(BasePubsubMessage):
    payload: StockTransferModel
    event: str
    quantity: int
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "pharmagob-stock-transfer-events"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {**default_attributes, "event": self.event}


@dataclass(kw_only=True)
class ShipmentsPubsubMessage(BasePubsubMessage):
    payload: ShipmentModel
    status: str
    review_status: str
    origin: str
    action_type: Optional[str] = None
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "pharmagob-shipments"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {
            **default_attributes,
            "status": self.status,
            "origin": self.origin,
            "review_status": self.review_status,
        }

@dataclass(kw_only=True)
class locationContentCloseEvents(BasePubsubMessage):
    payload: ShipmentDetailModel
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "location-content-close-events"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {
            **default_attributes,
        }



@dataclass(kw_only=True)
class ItemsPubsubMessage(BasePubsubMessage):
    payload: ItemModel
    origin: str
    action_type: str
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "pharmagob-items"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {
            **default_attributes,
            "origin": self.origin,
            "action_type": self.action_type,
        }



@dataclass(kw_only=True)
class PharmagobShipmentDetiailsPubsubMessage(BasePubsubMessage):
    payload: ShipmentModel
    status: str
    review_status: str
    origin: str
    action_type: Optional[str] = None
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "pharmagob-shipment-details"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {
            **default_attributes,
            "status": self.status,
            "origin": self.origin,
            "review_status": self.review_status,
        }