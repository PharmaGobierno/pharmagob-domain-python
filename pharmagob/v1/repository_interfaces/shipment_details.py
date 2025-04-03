from ._base import BaseRepositoryInterface


class ShipmentDetailRepositoryInterface(BaseRepositoryInterface):
    def get_by_shipment_id(self, shipment_id: str) -> list[dict]: ...

    pass
