from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ._base import UpdatableModel
from .minified import min_models


class Status(str, Enum):
    DISPATCHED = "DISPATCHED"
    PARTIAL_DISPATCHED = "PARTIAL_DISPATCHED"
    CANCELLED = "CANCELLED"


class DispatchCategory(str, Enum):
    MEDICATION = "MEDICATION"
    MEDICAL_SUPPLIES = "MEDICAL_SUPPLIES"
    MIXED = "MIXED"


@dataclass(kw_only=True)
class DispatchRecordModel(UpdatableModel):
    __entity_name__ = "dispatch-records"

    umu_id: str
    category: str
    reference_id: str
    dispatch_type: str
    dispatch_at: int
    service: str
    status: Status
    author: min_models.UserMin
    dispatch_details: Optional[List[min_models.DispatchRecordDetailMin]] = None
    dispatch_notes: Optional[str] = None
    prescribed_at: Optional[int] = None

    def minified(self) -> min_models.DispatchRecordMin:
        return min_models.DispatchRecordMin(
            id=self._id,
            umu_id=self.umu_id,
            reference_id=self.reference_id,
            dispatch_type=self.dispatch_type,
            dispatch_at=self.dispatch_at,
            service=self.service,
            category=self.category,
            prescribed_at=self.prescribed_at,
        )
