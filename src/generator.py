"""Deliberately low-quality, but standards-compliant, UUIDv4 generation."""

from __future__ import annotations

import time
import uuid


class LinearCongruentialGenerator:
    """A small 32-bit linear congruential generator."""

    MULTIPLIER = 1_664_525
    INCREMENT = 1_013_904_223
    MODULUS = 1 << 32

    def __init__(self, seed: int) -> None:
        if not isinstance(seed, int):
            raise TypeError("seed must be an integer")
        self.state = seed % self.MODULUS

    def next(self) -> int:
        self.state = (
            self.MULTIPLIER * self.state + self.INCREMENT
        ) % self.MODULUS
        return self.state


def biased_uuid4(generator: LinearCongruentialGenerator) -> uuid.UUID:
    """Return an RFC 9562 UUIDv4 built entirely from LCG output.

    ``uuid.UUID(..., version=4)`` overwrites the six structural bits, ensuring
    the version and RFC variant remain correct even for pathological states.
    """

    raw = 0
    for _ in range(4):
        raw = (raw << 32) | generator.next()
    return uuid.UUID(int=raw, version=4)


# An isolate keeps this state between requests when Cloudflare reuses it.
_generator = LinearCongruentialGenerator(time.time_ns())


def next_uuid() -> uuid.UUID:
    return biased_uuid4(_generator)
