from pharmagob.v1.models.warehouse import WarehouseModel
from pharmagob.v1.repository_interfaces.warehouses import WarehouseRepositoryInterface

from ._base import BaseService


class WarehouseService(BaseService[WarehouseModel, WarehouseRepositoryInterface]):
    __model__ = WarehouseModel
