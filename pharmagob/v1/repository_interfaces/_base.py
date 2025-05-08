from abc import ABCMeta, abstractmethod
from typing import Iterator, List, Optional, Tuple, Union


class BaseRepositoryInterface(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "create")
            and callable(subclass.create)
            and hasattr(subclass, "update")
            and callable(subclass.update)
            and hasattr(subclass, "set")
            and callable(subclass.set)
            and hasattr(subclass, "get")
            and callable(subclass.get)
            and hasattr(subclass, "get_paginated")
            and callable(subclass.get_paginated)
        )

    @abstractmethod
    def create(self, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id, *, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    def update_many(self, and_conditions: Optional[List[tuple]], *, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    def set(self, entity_id, *, data: dict, write_only_if_insert: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        entity_id: str,
        *,
        umu_id: Optional[str] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None,
    ) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_paginated(
        self,
        page: int,
        limit: int,
        *,
        umu_id: Optional[str] = None,
        and_conditions: Optional[List[tuple]] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[List[str]] = None,
    ) -> Tuple[int, Iterator[dict]]:
        raise NotImplementedError
