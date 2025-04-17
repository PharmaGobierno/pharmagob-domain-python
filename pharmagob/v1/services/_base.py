from typing import Generic, Iterator, List, Optional, Tuple, Type, TypeVar, Union

from pharmagob.v1.models._base import BaseModel
from pharmagob.v1.repository_interfaces._base import BaseRepositoryInterface

RepositoryInterfaceT = TypeVar("RepositoryInterfaceT", bound="BaseRepositoryInterface")
ModelT = TypeVar("ModelT", bound="BaseModel")


class BaseService(Generic[ModelT, RepositoryInterfaceT]):
    __model__: Type[ModelT]

    def __init__(self, repository: RepositoryInterfaceT):
        self.repository = repository

    def create(self, entity: ModelT) -> None:
        data = entity.dict()
        self.repository.create(data)

    def update(self, entity_id, *, entity: ModelT) -> int:
        data = entity.dict()
        return self.repository.update(entity_id, data=data)

    def set(
        self, entity_id, *, entity: ModelT, write_only_if_insert: bool = False
    ) -> int:
        data = entity.dict()
        return self.repository.set(
            entity_id, data=data, write_only_if_insert=write_only_if_insert
        )

    def get(
        self,
        entity_id,
        *,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None,
    ) -> ModelT:
        data: dict = self.repository.get(entity_id, sort=sort, projection=projection)
        return self.__model__(**data)

    def get_paginated(
        self,
        page: int,
        limit: int,
        *,
        and_conditions: Optional[List[tuple]] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[List[str]] = None,
    ) -> Tuple[int, Iterator[ModelT]]:
        count, result = self.repository.get_paginated(
            page, limit, and_conditions=and_conditions, sort=sort, projection=projection
        )
        return count, map(lambda itm: self.__model__(**itm), result)
