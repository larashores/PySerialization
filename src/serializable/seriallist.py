from serializable.serializable import Serializable
from serializable.serialint import SerialU32


def serial_list(list_type):
    """
    Returns a homogeneous Serializable list type of type list_type

    Arss:
        list_type: The Serializable type to store in the array
    """

    class _SerialList(list, Serializable):
        """A list type that can store homogeneous Serializable types."""
        array_type = property(lambda self: self._array_type)

        def __init__(self, values=[]):
            self.set(values)

        @staticmethod
        def _validate(value):
            """
            Validates an argument by confirming it is of list_type or trying to convert it to one

            Args:
                value: The value to validate
            """
            if not isinstance(value, list_type):
                try:
                    return list_type(value)
                except:
                    raise ValueError("'{}' is of type '{}', not '{}'".format(value, type(value), list_type))
            return value

        def append(self, value):
            """
            Adds a list_type object to the list

            Args:
                value: The list_type object
            """
            list.append(self, self._validate(value))

        def insert(self, ind, value):
            """
            Inserts a list_type object to the list

            Args:
                ind: The index to insert at
                value: The list_type object
            """
            list.insert(self, ind, self._validate(value))

        def set(self, values):
            """
            Sets the items of the SerialList to be equal to the list_type objects in an iterable

            Args:
                values: The list_type objects
            """
            for value in values:
                self._validate(value)
            self.clear()
            for value in values:
                self.append(value)

        def load_in_place(self, data, index=0):
            """Loads a SerialList by loading the number of objects as a U32 and then loading that many list_types"""
            self.clear()
            size, index = SerialU32.from_bytes(data, index)
            for _ in range(size.get()):
                obj, index = list_type.from_bytes(data, index)
                list.append(self, obj)
            return index

        def to_bytes(self):
            """Saves a SerialList by saving the number of objects as a U32 and then saving that many list_types"""
            size = SerialU32(len(self))
            data = size.to_bytes()
            for val in self:
                data += val.to_bytes()
            return data

    return _SerialList
