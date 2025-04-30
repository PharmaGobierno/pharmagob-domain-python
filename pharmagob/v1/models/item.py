from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel


@dataclass(kw_only=True)
class ItemModel(UpdatableModel):
    __entity_name__ = "items"

    foreign_id: str
    disabled: bool = False
    is_controlled: bool
    category: str
    sub_category: str
    clasification: str
    description: str
    short_description: Optional[str]
    name: Optional[str]
    controller_group: Optional[str]
    is_packing: Optional[bool]
    pieces_package: Optional[int]
    unit_price: Optional[float]
