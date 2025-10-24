from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel, uuid_by_params
from .minified import min_models


@dataclass(kw_only=True)
class DispatchRecordStatusModel(BaseModel):
    __entity_name__ = "dispatch-record-status"

    umu_id: str
    author: min_models.UserMin
    status: str
    dispatch_record: min_models.DispatchRecordMin
    origin_timestamp: int
    context: Optional[dict] = None

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(
            self.dispatch_record.id, self.umu_id, self.origin_timestamp
        )
