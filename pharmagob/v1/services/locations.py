from typing import Iterator, Tuple

from pharmagob.v1.models.location import LocationModel
from pharmagob.v1.repository_interfaces.locations import LocationRepositoryInterface

from ._base import BaseService


class LocationService(BaseService[LocationModel, LocationRepositoryInterface]):
    __model__ = LocationModel

    def __init__(self, repository: LocationRepositoryInterface):
        super().__init__(repository)

    def get_by_umu_id(self, umu_id: str) -> Tuple[int, Iterator[dict]]:
        return self.repository.get_by_umu_id(umu_id)
