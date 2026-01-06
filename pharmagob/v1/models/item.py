from dataclasses import dataclass
from typing import Optional

from ._base import UpdatableModel
from .minified.min_models import ItemMin

SHORT_DESCRIPTION_LENGTH = 250


@dataclass(kw_only=True)
class ItemModel(UpdatableModel):
    __entity_name__ = "items"

    foreign_id: str
    is_controlled: bool
    category: str
    sub_category: str
    clasification: str
    description: str
    disabled: bool = False
    short_description: Optional[str] = None
    controller_group: Optional[str] = None
    is_packing: Optional[bool] = None
    pieces_package: Optional[int] = None
    unit_price: Optional[float] = None

    def __builder_short_description(self) -> str:
        return self.description[:SHORT_DESCRIPTION_LENGTH].strip()

    def __post_init__(self):
        super().__post_init__()
        if self.short_description is None:
            self.short_description = self.__builder_short_description()

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
