from pharmagob.v1.models.location import LocationModel
from pharmagob.v1.repository_interfaces.locations import LocationRepositoryInterface

from ._base import BaseService


class LocationService(BaseService[LocationModel, LocationRepositoryInterface]):
    __model__ = LocationModel
