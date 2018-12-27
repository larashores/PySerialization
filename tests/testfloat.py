from pyserialization.serialfloat import SerialHalf, SerialFloat, SerialDouble

import unittest
import sys


def has_half_float_type():
    return sys.version_info[0] > 3 and sys.version_info[1] > 6


class TestSerialFloat(unittest.TestCase):
    def test_small(self):
        single = SerialFloat(10)
        double = SerialDouble(10)

        self.assertEqual(SerialFloat.from_bytes(single.to_bytes())[0].get(), 10)
        self.assertEqual(SerialDouble.from_bytes(double.to_bytes())[0].get(), 10)

        if has_half_float_type():
            half = SerialHalf(10)
            self.assertEqual(SerialHalf.from_bytes(half.to_bytes())[0].get(), 10)

    def test_size(self):
        single = SerialFloat(10)
        double = SerialDouble(10)

        self.assertEqual(len(single.to_bytes()), 4)
        self.assertEqual(len(double.to_bytes()), 8)

        if has_half_float_type():
            half = SerialHalf(10)
            self.assertEqual(len(half.to_bytes()), 2)
