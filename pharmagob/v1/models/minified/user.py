import uuid
from dataclasses import dataclass


@dataclass
class UserMin:
    id: uuid.UUID
    umu_id: str
    display_name: str
