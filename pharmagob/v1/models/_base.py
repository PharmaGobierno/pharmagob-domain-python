import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from time import time
from typing import Generic, Self, TypeVar

StateAttributeT = TypeVar("StateAttributeT", bound="Enum")


@dataclass
class BaseModel:
    _id: str = field(default_factory=lambda: str(uuid.UUID()))
    created_at: int = field(default_factory=lambda: int(time() * 1000))
    version: str = "1.0.0"

    @classmethod
    def get_entity_name(cls) -> str:
        if not getattr(cls, "__entity_name__", None):
            raise TypeError(
                f"__entity_name__ must be defined at " f"{cls.__class__.__name__} model"
            )
        return str(getattr(cls, "__entity_name__", None))

    def dict(self):
        return asdict(self)

    @classmethod
    def from_params(cls, **kwargs) -> Self:
        return cls(**kwargs)


@dataclass(kw_only=True)
class UpdatableModel:
    updated_at: int


@dataclass(kw_only=True)
class StatefulModel(Generic[StateAttributeT]):
    """A generic dataclass representing a stateful entity with
    transition timestamp and state.

    Attributes:
        transition_timestamp (int): The timestamp of the state
            transition.
        state (StateAttributeT): The current state of the entity.
    """

    transition_timestamp: int
    state: StateAttributeT
