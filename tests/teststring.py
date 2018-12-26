import unittest

from serializable.serialstring import SerialAsciiString, SerialString


class TestSerialInt(unittest.TestCase):
    def test_unicode(self):
        text = 'a\u0e55\u0e57a'
        string1 = SerialString(text)
        string2 = SerialString.from_bytes(string1.to_bytes())[0]
        self.assertEqual(string2.get(), text)
        self.assertRaises(ValueError, SerialAsciiString, text)

    def test_empty(self):
        text = ''
        string1 = SerialString(text)
        string1ascii = SerialAsciiString(text)
        string2 = SerialString.from_bytes(string1.to_bytes())[0]
        string2ascii = SerialString.from_bytes(string1ascii.to_bytes())[0]
        self.assertEqual(string2.get(), text)
        self.assertEqual(string2ascii.get(), text)

    def test_short(self):
        text = '!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        string1 = SerialString(text)
        string1ascii = SerialAsciiString(text)
        string2 = SerialString.from_bytes(string1.to_bytes())[0]
        string2ascii = SerialString.from_bytes(string1ascii.to_bytes())[0]
        self.assertEqual(string2.get(), text)
        self.assertEqual(string2ascii.get(), text)

    def test_long(self):
        text = 'abc' * 10000
        string1 = SerialString(text)
        string1ascii = SerialAsciiString(text)
        string2 = SerialString.from_bytes(string1.to_bytes())[0]
        string2ascii = SerialString.from_bytes(string1ascii.to_bytes())[0]
        self.assertEqual(string2.get(), text)
        self.assertEqual(string2ascii.get(), text)
