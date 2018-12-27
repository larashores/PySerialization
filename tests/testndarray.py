import unittest

try:
    import numpy as np
    numpy_installed = True
except ImportError:
    numpy_installed = False

if numpy_installed:
    from pyserialization.serialndarray import SerialNdArray


import unittest
import random


@unittest.skipIf(not numpy_installed, 'numpy not installed')
class TestSerialNdArray(unittest.TestCase):
    def test_dtypes(self):
        data_types = ['bool_', 'int_', 'intc', 'intp', 'int8', 'int16', 'int32', 'int64', 'uint8', 'uint16', 'uint32',
                      'int64', 'float_', 'float16', 'float32', 'float64', 'complex_', 'complex64', 'complex128']
        for data_type in data_types:
            array1 = SerialNdArray(np.ones(1, dtype=data_type))
            data = array1.to_bytes()
            array2 = SerialNdArray.from_bytes(data)[0]
            self.assertEqual(array2.get()[0], 1)

    def test_empty(self):
        array = np.zeros([])
        array1 = SerialNdArray(array)
        array2 = SerialNdArray.from_bytes(array1.to_bytes())[0]
        self.assertTrue(np.all(array == array2.get()))

    def test_long(self):
        array = np.array(np.array([random.random() for _ in range(40000)]))
        array1 = SerialNdArray(array)
        array2 = SerialNdArray.from_bytes(array1.to_bytes())[0]
        self.assertTrue(np.all(array == array2.get()))

    def test_many_dimensions(self):
        array = np.zeros([10, 10, 10])
        for i, j, k in np.ndindex(array.shape):
            array[i][j][k] = random.random()
        array1 = SerialNdArray(array)
        array2 = SerialNdArray.from_bytes(array1.to_bytes())[0]
        self.assertTrue(np.all(array == array2.get()))