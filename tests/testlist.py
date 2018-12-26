from serializable.seriallist import serial_list
from serializable.serialint import SerialU16

import unittest
import random

SerialU16List = serial_list(SerialU16)


class TestSerialList(unittest.TestCase):
    def test_empty(self):
        list1 = SerialU16List()
        list2 = SerialU16List.from_bytes(list1.to_bytes())[0]
        self.assertEqual(list2, [])

    def test_large(self):
        values = [SerialU16(int(random.random() * 100)) for _ in range(1000)]
        list1 = SerialU16List(values)
        list2 = SerialU16List.from_bytes(list1.to_bytes())[0]
        for value1, value2 in zip(list2, values):
            self.assertEqual(value1.get(), value2.get())

    def test_convertible_type(self):
        list1 = SerialU16List([3])
        list2 = SerialU16List.from_bytes(list1.to_bytes())[0]
        self.assertEqual(list2[0].get(), 3)

    def test_inconvertible_type(self):
        self.assertRaises(ValueError, SerialU16List, ['hello'])
