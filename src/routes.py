"""Route UUID requests to the requested low-quality generator."""

from collections.abc import Callable
import uuid

from generator import next_uuid as next_uuid32
from generator16 import next_uuid as next_uuid16
from generator8 import next_uuid as next_uuid8


_GENERATORS: dict[str, Callable[[], uuid.UUID]] = {
    "/": next_uuid16,
    "/16": next_uuid16,
    "/32": next_uuid32,
    "/8": next_uuid8,
}


def generator_for_path(path: str) -> Callable[[], uuid.UUID] | None:
    return _GENERATORS.get(path)
