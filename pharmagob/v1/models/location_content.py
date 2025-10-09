from dataclasses import dataclass

from ._base import UpdatableModel, uuid_by_params
from .minified import min_models


@dataclass(kw_only=True)
class LocationContentModel(UpdatableModel):
    __entity_name__ = "location-contents"

    umu_id: str
    lot: str
    expiration_date: int
    quantity: int
    item: min_models.ItemMin
    location: min_models.LocationMin
    last_author: min_models.UserMin

    def __post_init__(self):
        super().__post_init__()
        self._id = uuid_by_params(self.item.id, self.lot, self.location.id)
