from pharmagob.v1.models.location_content_event import LocationContentEventModel
from pharmagob.v1.repository_interfaces.location_content_events import (
    LocationContentEventsRepositoryInterface,
)

from ._base import BaseService


class LocationContentEventService(
    BaseService[LocationContentEventModel, LocationContentEventsRepositoryInterface]
):
    __model__ = LocationContentEventModel
