import unittest
import uuid
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from generator8 import LinearCongruentialGenerator8, biased_uuid4_8


class Generator8Tests(unittest.TestCase):
    def test_outputs_are_rfc_uuid4(self):
        generator = LinearCongruentialGenerator8(7)

        for _ in range(100):
            value = biased_uuid4_8(generator)
            self.assertEqual(value.version, 4)
            self.assertEqual(value.variant, uuid.RFC_4122)

    def test_seed_is_normalized_to_8_bits(self):
        modulus = LinearCongruentialGenerator8.MODULUS
        self.assertEqual(LinearCongruentialGenerator8(-1).state, modulus - 1)
        self.assertEqual(LinearCongruentialGenerator8(modulus).state, 0)

    def test_uuid_sequence_repeats_after_16_values(self):
        generator = LinearCongruentialGenerator8(42)
        first = biased_uuid4_8(generator)

        for _ in range(15):
            biased_uuid4_8(generator)

        self.assertEqual(biased_uuid4_8(generator), first)


if __name__ == "__main__":
    unittest.main()
