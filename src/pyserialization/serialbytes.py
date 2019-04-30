from pyserialization.serializable import Serializable
from pyserialization.serialint import SerialU32


class SerialBytes(Serializable):
    """A Serializable bytes object that also saved its length"""

    def __init__(self, value=bytes()):
        """initializes the SerialChar with an initial value of no bytes"""
        self.set(value)

    def __str__(self):
        """Returns the __str__ representation of the stored bytes"""
        return str(self._value)

    def get(self):
        """Returns the stored bytes"""
        return self._value

    def set(self, value):
        """
        Sets the value of the stored bytes

        Args:
            value: The bytes to store
        """
        if not isinstance(value, (bytes, bytearray)):
            raise ValueError("Value not bytes! {}".format(value))
        self._value = value

    def load_in_place(self, data, index=0):
        """Loads the size of the bytes object and the actual bytes"""
        size, index = SerialU32.from_bytes(data, index)
        self._value = data[index:index+size.get()]
        return index + size.get()

    def to_bytes(self):
        """Saves the size of the bytes object and then the bytes object"""
        size = SerialU32(len(self._value))
        data = size.to_bytes() + self._value
        return data


if __name__ == '__main__':
    data = b'adf432989ihadf'

    serial_data = SerialBytes(data)
    packed = serial_data.to_bytes()
    unpacked, index = SerialBytes.from_bytes(packed)
    print(unpacked.get())
