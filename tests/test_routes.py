import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from generator import next_uuid as next_uuid32
from generator16 import next_uuid as next_uuid16
from routes import generator_for_path


class RoutesTests(unittest.TestCase):
    def test_root_and_16_use_the_16_bit_generator(self):
        self.assertIs(generator_for_path("/"), next_uuid16)
        self.assertIs(generator_for_path("/16"), next_uuid16)

    def test_32_uses_the_32_bit_generator(self):
        self.assertIs(generator_for_path("/32"), next_uuid32)

    def test_unknown_path_has_no_generator(self):
        self.assertIsNone(generator_for_path("/unknown"))


if __name__ == "__main__":
    unittest.main()
