from pharmagob.v1.models.item_logs import ItemLogModel
from pharmagob.v1.repository_interfaces.item_logs import ItemLogRepositoryInterface

from ._base import BaseService


class ItemLogsService(BaseService[ItemLogModel, ItemLogRepositoryInterface]):
    __model__ = ItemLogModel
