from dataclasses import dataclass
from typing import Optional

from ._base import BaseModel, UpdatableModel


@dataclass(kw_only=True)
class ItemModel(BaseModel, UpdatableModel):
    __entity_name__ = "items"

    foreign_id: str
    disabled: bool = False
    name: str
    is_controlled: bool
    category: str
    controller_group: Optional[str]
    sub_category: Optional[str]
    clasification: Optional[str]
    description: Optional[str]
    short_description: Optional[str]
    is_packing: Optional[bool]
    pieces_package: Optional[int]
    unit_price: Optional[float]
