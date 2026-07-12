"""8-bit LCG variant of the deliberately low-quality UUID generator."""

from __future__ import annotations

import time
import uuid

from generator import LinearCongruentialGenerator


class LinearCongruentialGenerator8(LinearCongruentialGenerator):
    """An 8-bit LCG using the same recurrence as the 32-bit variant."""

    MODULUS = 1 << 8


def biased_uuid4_8(generator: LinearCongruentialGenerator8) -> uuid.UUID:
    """Return an RFC 9562 UUIDv4 assembled from sixteen 8-bit LCG outputs."""

    raw = 0
    for _ in range(16):
        raw = (raw << 8) | generator.next()
    return uuid.UUID(int=raw, version=4)


# An isolate keeps this state between requests when Cloudflare reuses it.
_generator = LinearCongruentialGenerator8(time.time_ns())


def next_uuid() -> uuid.UUID:
    return biased_uuid4_8(_generator)
