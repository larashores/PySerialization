from serializable.serializable import Serializable
from serializable.endianness import Endianess

import enum
import struct
import numbers


class _FloatInfo:
    """
    Used to store the info that describes the possible floating point types accepted by the struct module

    Properties:
        label = The character that represents the type in the struct format string
        size = The size of the floating point in bytes
    """
    label = property(lambda self: self._label)
    size = property(lambda self: self._size)

    def __init__(self, label, size):
        """
        Initializes the _FloatInfo with values that become read-only

        Args:
            label = The character that represents the type in the struct format string
            size = The size of the floating point in bytes
        """
        self._label = label
        self._size = size


class _FloatType(enum.Enum):
    """Enumerates the possible floating point types accepted by the struct module"""
    half = _FloatInfo('e', 2)
    float = _FloatInfo('f', 4)
    double = _FloatInfo('d', 8)


def _create_floating_point(float_type):
    """
    Returns a class type for a Serializable object of a of a single or double precision floating point type

    This function should not be used directly, as each call returns a distinct type. Consequently,
    _create_floating_point(_FloatTypes.double) != _create_floating_point(_FloatTypes.double), which can cause problems
    with composite types. Instead use the half, float, and double types specified in the top-level of this module.

    Args:
        float_type: A floating point type specified in the _FloatTypes enum.
    """
    if not isinstance(float_type, _FloatType):
        raise ValueError('Not a valid floating point type: ' + str(float_type))

    class _SerialFloatingPoint(Serializable):
        """
        A Serializable floating point type that is converted with the python struct module
        """

        def __init__(self, value=0, *, endian=Endianess.native):
            """
            Initializes the floating point type to be equal to 'value' and converted using endianess 'endian'.

            Args:
                value: The initial value of the floating point type
                endian: The endianness to store and load the type. The default is the native byte order
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
            Sets the value of the stored floating point

            Args:
                value: The floating point type to store
            """
            if not isinstance(value, numbers.Number):
                raise ValueError("Value not float! {}".format(value))
            self._value = float(value)

        def set_endianness(self, endian):
            """
            Sets the endianness of the floating point type

            Args:
                endian: The endianness to store and load the type. The default is the native byte order
            """
            self._format_string = endian.value + float_type.value.label

        def load_in_place(self, data, index=0):
            """Loads a floating point type using the struct module"""
            end_index = index + float_type.value.size
            self._value = struct.unpack(self._format_string, data[index:end_index])[0]
            return end_index

        def to_bytes(self):
            """Loads a floating point type using the struct module"""
            return struct.pack(self._format_string, self._value)

    return _SerialFloatingPoint

SerialHalf = _create_floating_point(_FloatType.half)
SerialFloat = _create_floating_point(_FloatType.float)
SerialDouble = _create_floating_point(_FloatType.double)
