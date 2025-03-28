from enum import Enum
from typing import Generic, TypeVar

from .base import BaseModel

StateAttributeT = TypeVar("StateAttributeT", bound="Enum")


class StatefulModel(BaseModel, Generic[StateAttributeT]):
    """A generic dataclass representing a stateful entity with
    transition timestamp and state.

    Attributes:
        transition_timestamp (PositiveInt): The timestamp of the state
            transition.
        state (StateAttributeT): The current state of the entity.
    """

    transition_timestamp: int
    state: StateAttributeT
