from serializable.serialfloat import SerialHalf, SerialFloat, SerialDouble

import unittest


class TestSerialInt(unittest.TestCase):
    def test_small(self):
        half = SerialHalf(10)
        single = SerialFloat(10)
        double = SerialDouble(10)

        self.assertEqual(SerialHalf.from_bytes(half.to_bytes())[0].get(), 10)
        self.assertEqual(SerialFloat.from_bytes(single.to_bytes())[0].get(), 10)
        self.assertEqual(SerialDouble.from_bytes(double.to_bytes())[0].get(), 10)

    def test_size(self):
        half = SerialHalf(10)
        single = SerialFloat(10)
        double = SerialDouble(10)

        self.assertEqual(len(half.to_bytes()), 2)
        self.assertEqual(len(single.to_bytes()), 4)
        self.assertEqual(len(double.to_bytes()), 8)
