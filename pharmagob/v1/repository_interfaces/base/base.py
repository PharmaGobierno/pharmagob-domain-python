from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union


class BaseRepositoryInterface(ABC):
    @abstractmethod
    def get(
        self,
        entity_id: str,
        *,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None
    ) -> dict: ...

    @abstractmethod
    def update(self, entity_id, data: dict, *, upsert: bool = False) -> int: ...

    @abstractmethod
    def create(self, data: dict) -> None: ...
