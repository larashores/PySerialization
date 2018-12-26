from pyserialization.serialint import SerialU8, SerialU16, SerialU32, SerialU64, SerialS8, SerialS16, SerialS32, SerialS64

import unittest


class TestSerialInt(unittest.TestCase):
    def setUp(self):
        self.u8 = SerialU8()
        self.u16 = SerialU16()
        self.u32 = SerialU32()
        self.u64 = SerialU64()
        self.s8 = SerialS8()
        self.s16 = SerialS16()
        self.s32 = SerialS32()
        self.s64 = SerialS64()

    def test_lower_range(self):
        self._range_check([0, 0, 0, 0], [-2**x for x in (7, 15, 31, 63)])

    def test_upper_range(self):
        self._range_check([2**x - 1 for x in (8, 16, 32, 64)], [2**x - 1 for x in (7, 15, 31, 63)])

    def test_out_of_range_lower(self):
        self._out_of_range_check([-1, -1, -1, -1], [-2**x - 1 for x in (7, 15, 31, 63)])

    def test_out_of_range_upper(self):
        self._out_of_range_check([2**x for x in (8, 16, 32, 64)], [2**x for x in (7, 15, 31, 63)])

    def _range_check(self, unsigned_ranges, signed_ranges):
        u8, u16, u32, u64 = unsigned_ranges
        s8, s16, s32, s64 = signed_ranges
        self.u8.set(u8)
        self.u16.set(u16)
        self.u32.set(u32)
        self.u64.set(u64)
        self.s8.set(s8)
        self.s16.set(s16)
        self.s32.set(s32)
        self.s64.set(s64)

        self.assertEqual(u8, SerialU8.from_bytes(self.u8.to_bytes())[0].get())
        self.assertEqual(u16, SerialU16.from_bytes(self.u16.to_bytes())[0].get())
        self.assertEqual(u32, SerialU32.from_bytes(self.u32.to_bytes())[0].get())
        self.assertEqual(u64, SerialU64.from_bytes(self.u64.to_bytes())[0].get())

        self.assertEqual(s8, SerialS8.from_bytes(self.s8.to_bytes())[0].get())
        self.assertEqual(s16, SerialS16.from_bytes(self.s16.to_bytes())[0].get())
        self.assertEqual(s32, SerialS32.from_bytes(self.s32.to_bytes())[0].get())
        self.assertEqual(s64, SerialS64.from_bytes(self.s64.to_bytes())[0].get())

    def _out_of_range_check(self, unsigned_ranges, signed_ranges):
        u8, u16, u32, u64 = unsigned_ranges
        s8, s16, s32, s64 = signed_ranges
        self.assertRaises(ValueError, self.u8.set, u8)
        self.assertRaises(ValueError, self.u16.set, u16)
        self.assertRaises(ValueError, self.u32.set, u32)
        self.assertRaises(ValueError, self.u64.set, u64)
        self.assertRaises(ValueError, self.s8.set, s8)
        self.assertRaises(ValueError, self.s16.set, s16)
        self.assertRaises(ValueError, self.s32.set, s32)
        self.assertRaises(ValueError, self.s64.set, s64)
