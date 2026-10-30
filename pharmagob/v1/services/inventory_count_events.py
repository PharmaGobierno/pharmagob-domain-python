from pharmagob.v1.models.inventory_count_event import InventoryCountEventModel
from pharmagob.v1.repository_interfaces.inventory_count_events import (
    InventoryCountEventRepositoryInterface,
)

from ._base import UmuScopedService


class InventoryCountEventService(
    UmuScopedService[InventoryCountEventModel, InventoryCountEventRepositoryInterface]
):
    __model__ = InventoryCountEventModel
