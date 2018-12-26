from abc import ABCMeta
import collections
import inspect

from serializable import Serializable
from serialint import SerialU8, SerialU16, SerialU32


class UnionMeta(ABCMeta):
    """
    Meta class that keeps track of an ordered list of class attributes to later be used by the Composite class.
    Adds all class attributes of type SaveableType to member __ordered__ of the class __dict__
    """
    @classmethod
    def __prepare__(mcs, name, bases):
        return collections.OrderedDict()

    def __new__(mcs, name, bases, classdict):
        for base in bases:
            if hasattr(base, '__ordered__'):
                for key in base.__ordered__:
                    classdict[key] = base.__dict__[key]
        classdict['__ordered__'] = [key for key in classdict.keys() if
                                    inspect.isclass(classdict[key]) and
                                    issubclass(classdict[key], Serializable)]
        classdict['__typemap__'] = {key: classdict[key] for key in classdict['__ordered__']}
        classdict['__revtypemap__'] = {classdict[key]: key for key in classdict['__ordered__']}

        return type.__new__(mcs, name, bases, dict(classdict))


class Union(Serializable, metaclass=UnionMeta):
    """
    A Saveable Composite type. This class is meant to be subclassed to easily create new SaveableType's made up of
    other SaveableTypes. For each type the object should hold, simply add a class attribute that is equal to that type.
    Every instance created will have a value of that type. No new instances attributes can be directly added. If the
    SaveableType has a 'get' method, then accessing that attribute will return its get method. If it has a 'set' method
    then setting that attribute will call its set method. Otherwise setting is disallowed

    The bytearray representation of a composite is each bytearray representation of the composite in the order they were
    declared, one after another

    Ex.
    class Composite1(Composite):
        val1 = saveable_int('u32')
        val2 = array('saveable_int('u32'))

        Every Composite1 that is created will have a val1 and val2 attributes of the specified types. val1 = 5 will call
        val1.set(5) but val2 does not have a set so val2 = [4] will cause an Exception


    """
    def __init__(self):
        """
        Creates an instance attribute for each type in the class attribute '__ordered__'.
        """
        Serializable.__init__(self)
        self._current = self.__typemap__[self.__ordered__[0]]()

    def __str__(self):
        """Returns string representation of current stored object"""
        return self._current.__str__()

    def get(self):
        """Returns the current stored object"""
        return self._current

    def get_type(self):
        """Returns the current stored type"""
        return type(self._current)

    def set(self, Type, value=None):
        """
        Sets the value of the union to a new type with an optional initial value

        Args:
            Type: The new type to store in this union
            value: A value of type 'Type' to set the union to
        """
        if Type in self.__revtypemap__:
            if value is None:
                self._current = Type()
            elif type(value) == Type:
                self._current = value
            else:
                raise ValueError('Value not {}! {}'.format(Type, value))
            return
        raise ValueError('Invalid Type {}'.format(Type))

    def __setattr__(self, key, value):
        """
        Catches all attribute setting. Only allows the setting if the attribute being set has a 'set' method. If it does
        calls attribute.set(value). Otherwise setting is disallowed
        """
        if key in self.__typemap__:
            Type = self.__typemap__[key]
            if not callable(getattr(Type, 'set', None)):
                raise ValueError("Cannot assign directly to '{}' ({})".format(key, type(Type)))
            if key != self.__revtypemap__[type(self._current)]:
                self.set(Type)
            self._current.set(value)
        else:
            Serializable.__setattr__(self, key, value)

    def __getattribute__(self, item):
        """
        Catches all attribute getting. If the attribute defines a 'get' method returns that instead, otherwise just
        returns the attribute
        """
        get_attribute = lambda item: Serializable.__getattribute__(self, item)
        if item not in get_attribute('__typemap__'):
            return get_attribute(item)
        current = get_attribute('__dict__')['__current__']
        SetType = get_attribute('__typemap__')[item]
        if type(current) != SetType:
            return None
        return current

    def load_in_place(self, data, index=0):
        """Loads the union type as an index into the possible types and then calls from_byte_array on that type"""
        type_ind, index = SerialU8.from_bytes(data, index)
        if not (0 <= type_ind.get() < len(self.__ordered__)):
            raise ValueError('Union index {} is out of range'.format(type_ind.get()))
        Type = self.__typemap__[self.__ordered__[type_ind.get()]]
        value, index = Type.from_bytes(data, index)
        self.set(Type, value)
        return index

    def to_bytes(self):
        """Stores the index of the current type as a U8 and then calls to_bytes on that type"""
        if self._current is None:
            raise ValueError('Union is null')
        type_ind = SerialU8(self.__ordered__.index(self.__revtypemap__[type(self._current)]))
        return type_ind.to_bytes() + self._current.to_bytes()
