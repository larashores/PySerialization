from serializable.serialenum import serial_enum

import unittest
import enum


class TestEnum(enum.Enum):
    A = 0
    B = 'a'
    C = int
    D = 34

SerialTestEnum = serial_enum(TestEnum)

class TestSerialEnum(unittest.TestCase):
    def test_default(self):
        a = SerialTestEnum()
        b = SerialTestEnum.from_bytes(a.to_bytes())[0]
        self.assertEqual(b.get(), TestEnum.A)
        self.assertEqual(b.get().value, 0)

    def test_change(self):
        a = SerialTestEnum(TestEnum.C)
        b = SerialTestEnum.from_bytes(a.to_bytes())[0]
        self.assertEqual(b.get(), TestEnum.C)
        self.assertEqual(b.get().value, int)

    def test_incorrect(self):
        self.assertRaises(ValueError, SerialTestEnum, 0)