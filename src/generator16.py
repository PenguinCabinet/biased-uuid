"""16-bit LCG variant of the deliberately low-quality UUID generator."""

from __future__ import annotations

import time
import uuid

from generator import LinearCongruentialGenerator


class LinearCongruentialGenerator16(LinearCongruentialGenerator):
    """A 16-bit LCG using the same recurrence as the 32-bit variant."""

    MODULUS = 1 << 16


def biased_uuid4_16(generator: LinearCongruentialGenerator16) -> uuid.UUID:
    """Return an RFC 9562 UUIDv4 assembled from eight 16-bit LCG outputs."""

    raw = 0
    for _ in range(8):
        raw = (raw << 16) | generator.next()
    return uuid.UUID(int=raw, version=4)


# An isolate keeps this state between requests when Cloudflare reuses it.
_generator = LinearCongruentialGenerator16(time.time_ns())


def next_uuid() -> uuid.UUID:
    return biased_uuid4_16(_generator)
