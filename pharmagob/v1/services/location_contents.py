from pharmagob.v1.models.location_content import LocationContentModel
from pharmagob.v1.repository_interfaces.location_contents import (
    LocationContentRepositoryInterface,
)

from ._base import BaseService


class LocationContentService(
    BaseService[LocationContentModel, LocationContentRepositoryInterface]
):
    __model__ = LocationContentModel
