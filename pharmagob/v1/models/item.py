from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel
from .minified.min_models import ItemMin


@dataclass(kw_only=True)
class ItemModel(UpdatableModel):
    __entity_name__ = "items"

    foreign_id: str
    is_controlled: bool
    category: str
    sub_category: str
    clasification: str
    description: str
    short_description: str
    disabled: bool = False
    controller_group: Optional[str] = None
    is_packing: Optional[bool] = None
    pieces_package: Optional[int] = None
    unit_price: Optional[float] = None

    def minified(self) -> ItemMin:
        return ItemMin(
            id=self._id,
            foreign_id=self.foreign_id,
            description=self.description,
            is_controlled=self.is_controlled,
            category=self.category,
            sub_category=self.sub_category,
            short_description=self.short_description,
        )
