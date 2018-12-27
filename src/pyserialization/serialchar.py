from pyserialization.serializable import Serializable

import struct


class SerialChar(Serializable):
    """A Serializable char type that is converted with the python struct module"""

    def __init__(self, value=chr(0)):
        """initializes the SerialChar with an initial value of the null char"""
        self._format_string = 'c'
        self.set(value)

    def __str__(self):
        """Returns the __str__ representation of the stored integer"""
        return self._value.__str__()

    def get(self):
        """Returns the stored char"""
        return self._value

    def set(self, value):
        """
        Sets the value of the stored char while also performing a range check

        Args:
            value: The char to store
        """
        if not isinstance(value, str):
            raise ValueError("Value not str! {}".format(value))
        if len(value) != 1:
            raise ValueError('Must only be one character')
        if ord(value) > 127:
            raise ValueError("Oridance '{}' of character '{}' is too large. Max='128'".format(ord(value), value))
        self._value = value

    def load_in_place(self, data, index=0):
        """Loads a character type using the struct module"""
        end_index = index + 1
        char = struct.unpack(self._format_string, data[index:end_index])[0]
        self._value = char.decode()
        return end_index

    def to_bytes(self):
        """Converts a character type using the struct module"""
        return bytearray(struct.pack(self._format_string, self._value.encode()))
