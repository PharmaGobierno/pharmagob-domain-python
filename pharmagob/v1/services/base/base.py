from typing import Generic, List, Optional, Tuple, TypeVar, Union

from pharmagob.v1.models.base.base import BaseModel
from pharmagob.v1.repository_interfaces.base.base import BaseRepositoryInterface

RepositoryInterfaceT = TypeVar("RepositoryInterfaceT", bound="BaseRepositoryInterface")
ModelT = TypeVar("ModelT", bound="BaseModel")


class BaseService(Generic[ModelT, RepositoryInterfaceT]):
    __model__: ModelT

    def __init__(self, repository: RepositoryInterfaceT):
        self.repository = repository

    def create(self, entity: ModelT) -> None:
        data = entity.dict()
        self.repository.create(data)

    def get(
        self,
        entity_id,
        *,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None,
    ) -> ModelT:
        data: dict = self.repository.get(entity_id, sort=sort, projection=projection)
        return self.__model__.from_params(**data)

    def update(self, entity_id, entity: ModelT, upsert: bool = False) -> int:
        data = entity.dict()
        return self.repository.update(entity_id, data, upsert=upsert)
