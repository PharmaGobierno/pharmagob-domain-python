from pharmagob.v1.models.item import ItemModel
from pharmagob.v1.repository_interfaces.items import ItemRepositoryInterface

from ._base import BaseService


class ItemService(BaseService[ItemModel, ItemRepositoryInterface]):

    pass
