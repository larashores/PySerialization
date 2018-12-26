from pyserialization.serializable import Serializable
from pyserialization.serialint import SerialU32
from pyserialization.seriallist import serial_list
from pyserialization.serialstring import SerialAsciiString

from operator import mul
import functools
import numpy as np


class _IntList(serial_list(SerialU32)):
    """List of int types for saving array shape"""
    pass


class SerialNdArray(Serializable):
    """
    Type for serializing a numpy.ndarray
    """
    def __init__(self, value=None):
        """
        Initializes the array with an empty ndarray or an existing ndarray
        """
        Serializable.__init__(self)
        if value is not None:
            self.set(value)
        else:
            self._array = np.zeros([])

    def __str__(self):
        """Returns the __str__ representation of the stored ndarray"""
        return self._array.__str__()

    def get(self):
        """Returns the stored ndarray"""
        return self._array

    def set(self, value):
        """S
        ets the SerialNdArray with an existing ndarray

        Args:
            value: The new ndarray to track
        """
        if not isinstance(value, np.ndarray):
            raise ValueError('Value must be of type ndarray, not {}'.format(type(value)))
        self._array = value

    def load_in_place(self, data, index=0):
        """
        Deserializes the ndarray

        Type is serialized by first saving the data type as a string, the number of elements in the flattened array, the
        data in the ndarray, and then a list of U32s giving the shape of the array.
        """
        data_type, index = SerialAsciiString.from_bytes(data, index)
        array_size, index = SerialU32.from_bytes(data, index)
        self._array = np.frombuffer(data, data_type.get(), array_size.get(), index)
        index += self._array.nbytes
        size_array, index = _IntList.from_bytes(data, index)
        self._array = np.reshape(self._array, [value.get() for value in size_array])
        return index

    def to_bytes(self):
        """
        Serializes the ndarray

        Type is serialized by first saving the data type as a string, the number of elements in the flattened array, the
        data in the ndarray, and then a list of U32s giving the shape of the array.
        """
        data = SerialAsciiString(str(self._array.dtype)).to_bytes()
        data += SerialU32(functools.reduce(mul, self._array.shape, 1)).to_bytes()
        data += self._array.tobytes()
        size_array = _IntList()
        for value in self._array.shape:
            size_array.append(value)
        data += size_array.to_bytes()
        return data
