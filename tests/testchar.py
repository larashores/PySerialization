from serializable.serialchar import SerialChar

import unittest


class TestSerialChar(unittest.TestCase):
    def test_empty(self):
        self.assertRaises(ValueError, SerialChar, '')

    def test_multiple(self):
        self.assertRaises(ValueError, SerialChar, 'aa')

    def test_null(self):
        text = chr(0)
        string1 = SerialChar(text)
        string2 = SerialChar.from_bytes(string1.to_bytes())[0]
        self.assertEqual(string2.get(), text)

    def test_max(self):
        text = chr(127)
        string1 = SerialChar(text)
        string2 = SerialChar.from_bytes(string1.to_bytes())[0]
        self.assertEqual(string2.get(), text)

    def test_out_of_range(self):
        self.assertRaises(ValueError, SerialChar, chr(128))
