import struct

from serializable.serializable import Serializable
from serializable.serialint import SerialU32


def _create_string(encoding='ascii'):
    """
    Returns a class type for a Serializable string saved with the 's' struct type.

    This function should not be used directly, as each call returns a distinct type. Consequently,
    _create_string('ascii') != _create_int('ascii'), which can cause problems with composite types. Instead
    use the SerialString and SerialAsciiString types specified in the top-level of this module.

    Args:
        encoding: Encoding to use when serializing the string
    """
    class _SerialString(Serializable):
        """
        A Serializable string type that is converted with the python struct module

        The string is represented as a 32-bit unsigned int denoting the length of the string data followed by the data
        in the specified encoding
        """

        def __init__(self, value=''):
            """
            Initializes the string to be equal to 'value'.

            Args:
                The initial value of the string
            """
            self._format_string = '{}s'
            self.set(value)

        def __str__(self):
            """Returns the __str__ representation of the stored string"""
            return self._value.__str__()

        def get(self):
            """Returns the stored string"""
            return self._value

        def set(self, value):
            """
            Sets the value of the stored string while also checking that it can be encoded correctly

            Args:
                value: The string to store
            """
            if not isinstance(value, str):
                raise ValueError("Value not str! {}".format(value))
            try:
                self._data = value.encode(encoding)
                self._value = value
            except UnicodeEncodeError as ex:
                raise ValueError("String '{}' cannot be encoded to encoding '{}'".format(value, encoding)) from ex

        def load_in_place(self, data, index=0):
            """Loads the string as a U32 length and then loads the decoded string data"""
            length, index = SerialU32.from_bytes(data, index)
            end_index = index + length.get()
            encoded = struct.unpack(self._format_string.format(length.get()), data[index:end_index])[0]
            self._value = encoded.decode(encoding)
            return end_index

        def to_bytes(self):
            """Serializes the string as a U32 length and the encoded string data"""
            length = SerialU32(len(self._data))
            return length.to_bytes() + struct.pack(self._format_string.format(length.get()), self._data)

    return _SerialString


SerialAsciiString = _create_string('ascii')
SerialString = _create_string('utf-8')
