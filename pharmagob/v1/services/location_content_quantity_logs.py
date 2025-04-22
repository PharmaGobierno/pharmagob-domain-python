from pharmagob.v1.models.location_content_quantity_log import (
    LocationContentQuantityLogModel,
)
from pharmagob.v1.repository_interfaces.location_content_quantity_logs import (
    LocationContentQuantityLogsRepositoryInterface,
)

from ._base import BaseService


class LocationContentQuantityLogService(
    BaseService[
        LocationContentQuantityLogModel, LocationContentQuantityLogsRepositoryInterface
    ]
):
    __model__ = LocationContentQuantityLogModel
