from serializable.serialunion import Union
from serializable.serialint import SerialU16, SerialU32
from serializable.serialstring import SerialString

import unittest


class TestUnion(Union):
    a = SerialU16
    b = SerialU32
    c = SerialString


class TestSerialEnum(unittest.TestCase):
    def test_default(self):
        union1 = TestUnion()
        union2 = TestUnion.from_bytes(union1.to_bytes())[0]
        self.assertEqual(union2.get().get(), 0)
        self.assertEqual(union2.get_type(), SerialU16)

    def test_set_value(self):
        union1 = TestUnion(SerialString, SerialString('hello'))
        union2 = TestUnion.from_bytes(union1.to_bytes())[0]
        self.assertEqual(union2.get().get(), 'hello')
        self.assertEqual(union2.get_type(), SerialString)

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
