from dataclasses import dataclass


@dataclass
class DispatchDetailMin:
    location_content_id: str
    item_id: str
    item_foreign_id: str
    quantity: int
