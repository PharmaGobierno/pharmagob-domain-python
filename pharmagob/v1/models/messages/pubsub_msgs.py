from dataclasses import asdict, dataclass, field
from time import time
from typing import Any, Dict, Optional

from pharmagob.v1.models.dispatch_record import DispatchRecordModel
from pharmagob.v1.models.dispatch_record_details import DispatchRecordDetailModel
from pharmagob.v1.models.inventory_count_event import Events as InventoryCountEvents
from pharmagob.v1.models.inventory_count_event import InventoryCountEventModel
from pharmagob.v1.models.inventory_count_line import InventoryCountLineModel
from pharmagob.v1.models.inventory_count_task import InventoryCountTaskModel
from pharmagob.v1.models.item import ItemModel
from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.models.minified import min_models
from pharmagob.v1.models.shipment import ShipmentModel
from pharmagob.v1.models.shipment_detail import ShipmentDetailModel
from pharmagob.v1.models.stock_transfer import StockTransferModel
from pharmagob.v1.models.reports import ReportRequestModel
from pharmagob.v1.models.shipment import ReviewStatus


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
    
@dataclass(kw_only=True)
class GlobalReportPubsubMessage(BasePubsubMessage):
    payload: ReportRequestModel 
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "global-report-events"
    

@dataclass(kw_only=True)
class ShipmentDetailLogPubsubMessage(BasePubsubMessage):
    payload: min_models.ShipmentMin
    review_status: ReviewStatus
    origin: str
    origin_timestamp: int
    action_type: str
    version: str = "1"
    context: Optional[dict] = None

    @classmethod
    def topic(cls) -> str:
        return "shipment-details-logs"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {
            **default_attributes,
            "review_status": self.review_status,
        }


@dataclass(kw_only=True)
class InventoryCountTaskReleasePubsubMessage(BasePubsubMessage):
    """Carries the whole task (umu_id, count_type, count_scope,
    is_zero_stock_included, item_filter) so the release subscriber does not
    read the task again. event_id is the one of the TASK_RELEASED event."""

    payload: InventoryCountTaskModel
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "inventory-count-task-release"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        event = InventoryCountEvents.TASK_RELEASED
        return {
            **default_attributes,
            "umu_id": self.payload.umu_id,
            "task_id": self.payload._id,
            "event": event.value,
            "event_id": InventoryCountEventModel.generate_event_id(
                event, task_id=self.payload._id
            ),
        }


@dataclass(kw_only=True)
class InventoryCountEventsPubsubMessage(BasePubsubMessage):
    """event_id is the deterministic _id of the payload, the events
    subscriber persists it with set(write_only_if_insert=True)."""

    payload: InventoryCountEventModel
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "inventory-count-events"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        return {
            **default_attributes,
            "umu_id": self.payload.umu_id,
            "task_id": self.payload.task.id if self.payload.task else "",
            "event": InventoryCountEvents(self.payload.event).value,
            "event_id": self.payload._id,
        }


@dataclass(kw_only=True)
class InventoryCountAdjustmentAppliedPubsubMessage(BasePubsubMessage):
    """Applied adjustment of a line (resolution.adjustment_quantity) to be
    propagated to location-content-events by the adapter."""

    payload: InventoryCountLineModel
    event: str  # ADJUSTMENT_POSITIVE | ADJUSTMENT_NEGATIVE
    location_content: Optional[LocationContentModel] = None  # state after the $inc
    version: str = "1"

    @classmethod
    def topic(cls) -> str:
        return "inventory-count-adjustment-applied"

    def get_attributes(self) -> Dict[str, str]:
        default_attributes = super().get_attributes()
        event = InventoryCountEvents(self.event)
        return {
            **default_attributes,
            "umu_id": self.payload.umu_id,
            "task_id": self.payload.task.id,
            "event": event.value,
            "event_id": InventoryCountEventModel.generate_event_id(
                event, line_id=self.payload._id
            ),
        }
