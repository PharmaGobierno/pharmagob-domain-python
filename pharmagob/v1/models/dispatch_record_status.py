from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import BaseModel, uuid_by_params
from .minified import min_models


class QuantityActionType(str, Enum):
    INCREASE = "INCREASE"
    SUBTRACT = "SUBTRACT"


@dataclass(kw_only=True)
class DispatchRecordStatusModel(BaseModel):
    __entity_name__ = "dispatch-record-status"

    umu_id: str
    author: min_models.UserMin
    dispatch_record: min_models.DispatchRecordMin
    origin_timestamp: int
    context: Optional[dict] = None

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(
            self.dispatch_record.id, self.umu_id, self.origin_timestamp
        )
