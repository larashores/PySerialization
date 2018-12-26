import struct
import enum

from serializable.endianness import Endianess
from serializable.serializable import Serializable


class _IntInfo:
    """
    Used to store the info that describes the possible integer types accepted by the struct module

    Properties:
        label = The character that represents the type in the struct format string
        size = The size of the integer in bytes
        range = A pair of minimum and maximum values for the particular integer type
    """
    label = property(lambda self: self._label)
    size = property(lambda self: self._size)
    range = property(lambda self: self._range)

    def __init__(self, label, size, int_range):
        """
        Initializes the _IntInfo with values that become read-only

        Args:
            label = The character that represents the type in the struct format string
            size = The size of the integer in bytes
            range = A pair of minimum and maximum values for the particular integer type
        """
        self._label = label
        self._size = size
        self._range = int_range


class _IntType(enum.Enum):
    """Enumerates the possible integer types accepted by the struct module"""
    U8 = _IntInfo('B', 1, (0, 255))
    U16 = _IntInfo('H', 2, (0, 65535))
    U32 = _IntInfo('I', 4, (0, 4294967295))
    U64 = _IntInfo('Q', 8, (0, 18446744073709551615))
    S8 = _IntInfo('b', 1, (-128, 127))
    S16 = _IntInfo('h', 2, (-32768, 32767))
    S32 = _IntInfo('i', 4, (-2147483648, 2147483647))
    S64 = _IntInfo('q', 8, (-9223372036854775808, 9223372036854775807))


def _create_int(int_type):
    """
    Returns a class type for a Serializable object of an integer of a specific c-type.

    This function should not be used directly, as each call returns a distinct type. Consequently,
    _create_int(_IntTypes.U8) != _create_int(_IntTypes.U8), which can cause problems with composite types. Instead
    use the U8, U16, U32, S8, S16, and S32 types specified in the top-level of this module.

    Args:
        int_type: Any integer type specified in the _IntTypes enum.
    """
    if not isinstance(int_type, _IntType):
        raise ValueError('Not a valid int type: ' + str(int_type))

    class _SerialInt(Serializable):
        """
        A Serializable int type that is converted with the python struct module
        """

        def __init__(self, value=0, *, endian=Endianess.native):
            """
            Initializes the integer to be equal to 'value' and converted using endianess 'endian'.

            Args:
                The initial value of the integer
                The endianness to store and load the integer. The default is the native byte order
            """
            self.set(value)
            self.set_endianness(endian)

        def __str__(self):
            """Returns the __str__ representation of the stored integer"""
            return self._value.__str__()

        def __repr__(self):
            """Returns the __repr__ representation of the stored integer"""
            return self._value.__repr__()

        def get(self):
            """Returns the stored integer"""
            return self._value

        def set(self, value):
            """
            Sets the value of the stored integer while also performing a range check

            Args:
                value: The integer to store
            """
            if not isinstance(value, int):
                raise ValueError("Value not int! {}".format(value))
            _min, _max = int_type.value.range
            if value < _min:
                raise ValueError("Int {} is too small. Min={}".format(value, _min))
            if value > _max:
                raise ValueError("Int {} is too large. Max={}".format(value, _max))
            self._value = value

        def set_endianness(self, endian):
            """
            Sets the endianness of the floating point type

            Args:
                endian: The endianness to store and load the type. The default is the native byte order
            """
            self._format_string = endian.value + int_type.value.label

        def load_in_place(self, data, index=0):
            """Loads a SerialInt type using the struct module"""
            end_index = index + int_type.value.size
            self._value = struct.unpack(self._format_string, data[index:end_index])[0]
            return end_index

        def to_bytes(self):
            """Loads a SerialInt type using the struct module"""
            return struct.pack(self._format_string, self._value)

    return _SerialInt


SerialU8 = _create_int(_IntType.U8)
SerialU16 = _create_int(_IntType.U16)
SerialU32 = _create_int(_IntType.U32)
SerialU64 = _create_int(_IntType.U64)
SerialS8 = _create_int(_IntType.S8)
SerialS16 = _create_int(_IntType.S16)
SerialS32 = _create_int(_IntType.S32)
SerialS64 = _create_int(_IntType.S64)
