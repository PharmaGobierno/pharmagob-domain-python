from pharmagob.v1.models.stock_transfer import StockTransferModel
from pharmagob.v1.repository_interfaces.stock_transfers import (
    StockTransferRepositoryInterface,
)

from ._base import BaseService


class StockTransferService(
    BaseService[StockTransferModel, StockTransferRepositoryInterface]
):
    __model__ = StockTransferModel
