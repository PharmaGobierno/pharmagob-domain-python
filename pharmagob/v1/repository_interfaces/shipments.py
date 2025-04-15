from abc import abstractmethod
from typing import Iterator, List, Optional, Tuple

from ._base import BaseRepositoryInterface


class ShipmentRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def query_paginated(
        self,
        page: Optional[int] = None,
        and_conditions: Optional[List[tuple]] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        limit: Optional[int] = None,
    ) -> Tuple[int, Iterator[dict]]:
        raise NotImplementedError
