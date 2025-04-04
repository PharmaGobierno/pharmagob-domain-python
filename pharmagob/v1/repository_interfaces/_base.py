from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple, Union


class BaseRepositoryInterface(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get")
            and callable(subclass.get)
            and hasattr(subclass, "update")
            and callable(subclass.update)
            or hasattr(subclass, "create")
            and callable(subclass.create)
            or NotImplemented
        )

    @abstractmethod
    def create(self, data: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id, *, data: dict) -> int:
        raise NotImplementedError

    @abstractmethod
    def set(self, entity_id, *, data: dict, write_only_if_insert: bool = False) -> int:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        entity_id: str,
        *,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None
    ) -> dict:
        raise NotImplementedError
