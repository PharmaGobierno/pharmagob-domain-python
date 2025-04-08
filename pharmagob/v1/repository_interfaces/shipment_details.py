from abc import abstractmethod
from typing import Iterator, List, Optional, Tuple, Union

from ._base import BaseRepositoryInterface


class ShipmentDetailRepositoryInterface(BaseRepositoryInterface):
    @abstractmethod
    def get_by_shipment_id(
        self,
        shipment_id,
        *,
        sort: Optional[List[Tuple[str, int]]] = None,
        projection: Optional[Union[list, dict]] = None,
        limit: Optional[int] = None,
    ) -> Tuple[int, Iterator[dict]]:
        raise NotImplementedError
