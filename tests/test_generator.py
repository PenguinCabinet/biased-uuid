import unittest
import uuid
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from generator import LinearCongruentialGenerator, biased_uuid4


class GeneratorTests(unittest.TestCase):
    def test_corner_seeds_always_produce_rfc_uuid4(self):
        seeds = (
            0,
            1,
            -1,
            LinearCongruentialGenerator.MODULUS - 1,
            LinearCongruentialGenerator.MODULUS,
            10**100,
        )
        for seed in seeds:
            with self.subTest(seed=seed):
                value = biased_uuid4(LinearCongruentialGenerator(seed))
                self.assertEqual(uuid.UUID(str(value)), value)
                self.assertEqual(value.version, 4)
                self.assertEqual(value.variant, uuid.RFC_4122)

    def test_seed_is_normalized_at_both_ends(self):
        modulus = LinearCongruentialGenerator.MODULUS
        self.assertEqual(LinearCongruentialGenerator(-1).state, modulus - 1)
        self.assertEqual(LinearCongruentialGenerator(modulus).state, 0)

    def test_non_integer_seed_is_rejected(self):
        with self.assertRaises(TypeError):
            LinearCongruentialGenerator("0")

    def test_sequence_is_deterministic_and_advances(self):
        left = LinearCongruentialGenerator(42)
        right = LinearCongruentialGenerator(42)
        sequence = [biased_uuid4(left) for _ in range(20)]

        self.assertEqual(sequence, [biased_uuid4(right) for _ in range(20)])
        self.assertEqual(len(set(sequence)), len(sequence))

    def test_uuid_structure_is_applied_to_lcg_output(self):
        generator = LinearCongruentialGenerator(7)

        for _ in range(1_000):
            value = biased_uuid4(generator)
            self.assertEqual(value.version, 4)
            self.assertEqual(value.variant, uuid.RFC_4122)


if __name__ == "__main__":
    unittest.main()
