from dataclasses import asdict, dataclass, field, fields, is_dataclass
from enum import Enum
from time import time
from typing import Generic, List, TypeVar, Union, get_args, get_origin, get_type_hints
from uuid import NAMESPACE_OID, uuid4, uuid5

StateAttributeT = TypeVar("StateAttributeT", bound="Enum")


def uuid_by_params(*args):
    """Generates a UUIDv5 based on the given parameters.

    Args:
        *args: Variable number of arguments used to create the UUID.

    Returns:
        str: The generated UUID as a string.
    """
    value = "#".join(map(str, args))
    return str(uuid5(namespace=NAMESPACE_OID, name=value))


class DictModelMixin:
    @classmethod
    def from_dict(cls, data: dict):
        if not is_dataclass(cls):
            raise TypeError(f"{cls.__name__} it is not dataclass")

        field_types = get_type_hints(cls)
        init_values = {}

        for f in fields(cls):
            field_value = data.get(f.name)
            field_type = field_types.get(f.name)
            origin = get_origin(field_type)

            if field_value is None:
                init_values[f.name] = None
                continue

            if origin is Union:
                args = get_args(field_type)
                non_none_type = next(
                    (arg for arg in args if arg is not type(None)), None
                )
                if (
                    is_dataclass(non_none_type)
                    and hasattr(non_none_type, "from_dict")
                    and isinstance(field_value, dict)
                ):
                    init_values[f.name] = non_none_type.from_dict(field_value)
                else:
                    init_values[f.name] = field_value

            elif origin in (list, List):
                inner_type = get_args(field_type)[0]
                if is_dataclass(inner_type) and hasattr(inner_type, "from_dict"):
                    init_values[f.name] = [
                        inner_type.from_dict(i) if isinstance(i, dict) else i
                        for i in field_value
                    ]
                else:
                    init_values[f.name] = field_value

            elif (
                is_dataclass(field_type)
                and hasattr(field_type, "from_dict")
                and isinstance(field_value, dict)
            ):
                init_values[f.name] = field_type.from_dict(field_value)

            else:
                init_values[f.name] = field_value

        return cls(**init_values)


@dataclass
class BaseModel(DictModelMixin):
    _id: str = field(default_factory=lambda: str(uuid4()))
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


@dataclass(kw_only=True)
class UpdatableModel:
    updated_at: int = field(default_factory=lambda: int(time() * 1000))


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
