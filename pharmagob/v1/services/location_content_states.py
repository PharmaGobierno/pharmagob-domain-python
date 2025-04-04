from pharmagob.v1.models.location_content_state import LocationContentStateModel
from pharmagob.v1.repository_interfaces.location_content_states import (
    LocationContentStatesRepositoryInterface,
)

from ._base import BaseService


class LocationContentStateService(
    BaseService[LocationContentStateModel, LocationContentStatesRepositoryInterface]
):

    pass
