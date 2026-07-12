import unittest
import uuid
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from generator16 import LinearCongruentialGenerator16, biased_uuid4_16


class Generator16Tests(unittest.TestCase):
    def test_outputs_are_rfc_uuid4(self):
        generator = LinearCongruentialGenerator16(7)

        for _ in range(1_000):
            value = biased_uuid4_16(generator)
            self.assertEqual(value.version, 4)
            self.assertEqual(value.variant, uuid.RFC_4122)

    def test_seed_is_normalized_to_16_bits(self):
        modulus = LinearCongruentialGenerator16.MODULUS
        self.assertEqual(LinearCongruentialGenerator16(-1).state, modulus - 1)
        self.assertEqual(LinearCongruentialGenerator16(modulus).state, 0)

    def test_uuid_sequence_repeats_after_8192_values(self):
        generator = LinearCongruentialGenerator16(42)
        first = biased_uuid4_16(generator)

        for _ in range((1 << 13) - 1):
            biased_uuid4_16(generator)

        self.assertEqual(biased_uuid4_16(generator), first)


if __name__ == "__main__":
    unittest.main()
