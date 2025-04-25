from dataclasses import dataclass
from enum import Enum

from ._base import UpdatableModel
from .minified import min_properties


class Status(str, Enum):
    DISPATCHED = "DISPATCHED"


class DispatchType(str, Enum):
    INHOSPITAL_DISPENSING = "INHOSPITAL_DISPENSING"
    PRESCRIPTION = "PRESCRIPTION"


@dataclass(kw_only=True)
class DispatchRecordModel(UpdatableModel):
    __entity_name__ = "dispatch-records"

    umu_id: str
    dispatch_type: DispatchType
    status: Status = Status.DISPATCHED
    dispatch_details: list[min_properties.DispatchDetailMin]
    # TODO: agregar las demas propiedades
