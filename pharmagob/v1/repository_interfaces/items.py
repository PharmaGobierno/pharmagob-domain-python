from abc import abstractmethod
from typing import Iterator, List, Optional, Tuple, Union

from ._base import BaseRepositoryInterface


class ItemRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def get_by_foreign_id(
        self,
        foreign_id,
        *,
        umu_id: Optional[str] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None,
        limit: Optional[int] = None,
    ) -> Tuple[int, Iterator[dict]]:
        raise NotImplementedError
