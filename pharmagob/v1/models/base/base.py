import uuid
from dataclasses import asdict, dataclass
from typing import Self


@dataclass
class BaseModel:
    __entity_name__: str

    _id: uuid.UUID
    created_at: int
    version: str = "1.0.0"

    @classmethod
    def get_entity_name(cls) -> str:
        if not getattr(cls, "__entity_name__", None):
            raise TypeError(
                f"__entity_name__ must be defined at " f"{cls.__class__.__name__} model"
            )
        return cls.__entity_name__

    def dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

    @classmethod
    def from_params(cls, **kwargs) -> Self:
        return cls(**kwargs)
