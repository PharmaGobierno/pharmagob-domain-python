from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import BaseModel
from .minified import min_models


class QuantityActionType(str, Enum):
    INCREASE = "INCREASE"
    SUBTRACT = "SUBTRACT"


@dataclass(kw_only=True)
class AdministrativeIssueRecordModel(BaseModel):
    __entity_name__ = "administrative-issue-records"

    reference_id: str
    umu_id: str
    issue_category: list[str]
    issue_at: int
    author: min_models.UserMin
    location_content: min_models.LocationContentMin
    item: min_models.ItemMin
    quantity: int
    quantity_action_type: QuantityActionType
    origin_timestamp: int
    issue_notes: Optional[str] = None
