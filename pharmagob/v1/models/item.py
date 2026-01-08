from dataclasses import dataclass
from typing import Optional, Union

from ._base import UpdatableModel
from .minified.min_models import ItemMin

SHORT_DESCRIPTION_LENGTH = 250


class _AutoShortDescription:
    """sentinel for auto-generating short description"""

    pass


AUTO_SHORT = _AutoShortDescription()


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
    short_description: Union[str, _AutoShortDescription] = AUTO_SHORT
    controller_group: Optional[str] = None
    is_packing: Optional[bool] = None
    pieces_package: Optional[int] = None
    unit_price: Optional[float] = None

    def __builder_short_description(self, description: str) -> str:
        return description[:SHORT_DESCRIPTION_LENGTH].strip()

    def __post_init__(self):
        """override"""
        super().__post_init__()
        if self.short_description is AUTO_SHORT:
            self.short_description = self.__builder_short_description(self.description)

    def update(self, data: dict):
        """override"""
        description_updated = "description" in data
        short_description_passed = "short_description" in data
        if (
            description_updated and not short_description_passed
        ) or self.short_description is AUTO_SHORT:
            data["short_description"] = self.__builder_short_description(
                data["description"]
            )
        super().update(data)

    def minified(self) -> ItemMin:
        return ItemMin(
            id=self._id,
            foreign_id=self.foreign_id,
            description=self.description,
            is_controlled=self.is_controlled,
            category=self.category,
            sub_category=self.sub_category,
            short_description=(
                str(self.short_description)
                if not isinstance(self.short_description, _AutoShortDescription)
                else ""
            ),
        )
