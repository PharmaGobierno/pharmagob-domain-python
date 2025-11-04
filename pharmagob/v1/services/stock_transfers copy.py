from pharmagob.v1.models.stock_transfer_event import StockTransferEventModel
from pharmagob.v1.repository_interfaces.stock_transfer_events import (
    StockTransferEventRepositoryInterface,
)

from ._base import BaseService


class StockTransferService(
    BaseService[StockTransferEventModel, StockTransferEventRepositoryInterface]
):
    __model__ = StockTransferEventModel
