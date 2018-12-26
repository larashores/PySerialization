import enum

from serializable import Serializable
from serializable.serialint import SerialU32


def serial_enum(enum_type):
    """
    Creates a SerialEnum object that can hold one value of the types specified in an enum

    eg.

    class MyEnum(enum.Enum):
        A = 'enum_a'
        B = 'enum_b'
    MySerialEnum = serial_enum(MyEnum)
    a = MySerialEnum(MyEnum.B)
    """
    if not issubclass(enum_type, enum.Enum):
        raise ValueError('Argument must be int enum:', enum_type)

    class SerialEnum(Serializable):
        """Serial enum type that stores a single enum selected from 'enum_type'"""

        def __init__(self, value=list(enum_type.__members__.values())[0]):
            """
            Initializes the SerialEnum with a given enum or the first enum in enum_type.__members__
            """
            self.set(value)

        def get(self):
            """Returns the selected enum"""
            return self._value

        def set(self, value):
            """
            Sets the selected enum

            args:
                value: The new enum value
            """
            if not isinstance(value, enum_type):
                raise ValueError('Value must be enum type of {}'.format(enum_type))
            self._value = value

        def load_in_place(self, data, index=0):
            """Loads a U32 representing the index of the enum in enum_type"""
            position, index = SerialU32.from_bytes(data, index)
            self._value = list(enum_type.__members__.values())[position.get()]
            return index

        def to_bytes(self):
            """Saves the index of the enum in enum_type as a U32"""
            position = list(enum_type.__members__.keys()).index(self._value.name)
            return SerialU32(position).to_bytes()

    return SerialEnum
