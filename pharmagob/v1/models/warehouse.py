from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ._base import UpdatableModel


class WarehouseTypes(str, Enum):
    PHARMA = "PHARMA"
    SUBPHARMA = "SUBPHARMA"


@dataclass(kw_only=True)
class WarehouseModel(UpdatableModel):
    __entity_name__ = "warehouses"

    umu_id: str
    name: str
    type: str  # WarehouseTypes
    code: str
    description: Optional[str]
    addrress: Optional[str]
    disabled: bool = False
