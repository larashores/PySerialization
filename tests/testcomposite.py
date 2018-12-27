from pyserialization.composite import Composite
from pyserialization.serialint import SerialU16, SerialU32
from pyserialization.serialstring import SerialString

import unittest


class TestComposite(Composite):
    a = SerialU16
    b = SerialU32
    c = SerialString


class TestSerialComposite(unittest.TestCase):
    def test_all(self):
        composite1 = TestComposite()
        composite1.a = 4
        composite1.b = 5
        composite1.c = 'apple'
        composite2 = TestComposite.from_bytes(composite1.to_bytes())[0]
        self.assertEqual(composite2.a, 4)
        self.assertEqual(composite2.b, 5)
        self.assertEqual(composite2.c, 'apple')

    def test_set_wrong_type(self):
        composite = TestComposite()
        def set_a(value):
            composite.a = value
        self.assertRaises(ValueError, set_a, 'a')