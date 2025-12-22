from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel, uuid_by_params
from .minified import min_models


@dataclass(kw_only=True)
class ItemLogModel(BaseModel):
    __entity_name__ = "item-logs"

    item: dict
    origin_timestamp: int
    origin: str
    action_type: str
    author: Optional[min_models.UserMin] = None
    umu_id: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.item["_id"], self.origin_timestamp)
