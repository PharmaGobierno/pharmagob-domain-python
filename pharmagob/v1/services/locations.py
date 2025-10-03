from typing import Iterator, Tuple

from pharmagob.v1.models.location import LocationModel
from pharmagob.v1.repository_interfaces.locations import LocationRepositoryInterface

from ._base import BaseService


class LocationService(BaseService[LocationModel, LocationRepositoryInterface]):
    __model__ = LocationModel

    def get_by_umu_id(
        self, umu_id: str, *, limit: int = 100000
    ) -> Tuple[int, Iterator[LocationModel]]:
        count, result = self.repository.get_by_umu_id(umu_id, limit=limit)
        return count, map(lambda r: LocationModel(**r), result)
