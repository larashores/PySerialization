from pyserialization.union import Union
from pyserialization.serialint import SerialU16, SerialU32
from pyserialization.serialstring import SerialString

import unittest


class TestUnion(Union):
    a = SerialU16
    b = SerialU32
    c = SerialString


class TestSerialUnion(unittest.TestCase):
    def test_default(self):
        union1 = TestUnion()
        union2 = TestUnion.from_bytes(union1.to_bytes())[0]
        self.assertEqual(union2.get().get(), 0)
        self.assertEqual(union2.get_type(), SerialU16)
        self.assertEqual(union2.a, 0)
        self.assertRaises(ValueError, lambda: union2.b)

    def test_set_value(self):
        union1 = TestUnion(SerialString, SerialString('hello'))
        union2 = TestUnion.from_bytes(union1.to_bytes())[0]
        self.assertEqual(union2.get().get(), 'hello')
        self.assertEqual(union2.get_type(), SerialString)
        self.assertEqual(union2.c, 'hello')
        self.assertRaises(ValueError, lambda: union2.b)

    def test_set_convertible_value(self):
        union1 = TestUnion(SerialU32, 4)
        union2 = TestUnion.from_bytes(union1.to_bytes())[0]
        self.assertEqual(union2.get().get(), 4)
        self.assertEqual(union2.get_type(), SerialU32)

    def test_set_inconvertible_value(self):
        self.assertRaises(ValueError, TestUnion, SerialU32, 'a')

    def test_set_bad_type(self):
        self.assertRaises(ValueError, TestUnion, int)

    def test_set_good_type(self):
        union1 = TestUnion(SerialString)
        union2 = TestUnion.from_bytes(union1.to_bytes())[0]
        self.assertEqual(union2.get().get(), '')
        self.assertEqual(union2.get_type(), SerialString)
