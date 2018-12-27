from pyserialization.serializable import Serializable

from abc import ABCMeta
import collections
import inspect


class CompositeMeta(ABCMeta):
    """
    Meta class that keeps track of an ordered list of class attributes to later be used by the Composite class.

    Adds all class attributes of type Serializable type to member __ordered__ of the class __dict__
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

        return type.__new__(mcs, name, bases, dict(classdict))


class Composite(Serializable, metaclass=CompositeMeta):
    """
    A Serializable type that represents a composite of other Serializeable types.

    This class is meant to be subclassed to easily create new Serializable's made up of other Serializable's. For each
    type the object should hold, simply add a class attribute with a value of that type. Every instance created will
    automatically hold a value of that type with the name of the attribute. If one of the composite types has a 'get'
    method, then accessing that attribute will return the result of its get method. If the attribute has a 'set' method
    then setting that attribute will call its set method; otherwise setting is disallowed.

    The bytearray representation of a Composite is each bytearray representation of the composite in the order they were
    declared, one after another

    Ex.
    class Composite1(Composite):
        val1 = SerialU32
        val2 = array(SerialU32)

        Every Composite1 that is created will have val1 and val2 attributes of the specified types. Running val1 = 5
        will call val1.set(5) but val2 does not have a set methohd so val2 = [4] will raise an Exception.
    """

    def __init__(self):
        """
        Creates an instance attribute for each type in the class attribute '__ordered__'.
        """
        Serializable.__init__(self)
        for key, Type in self.__typemap__.items():
            self.__dict__[key] = Type()

    def __str__(self):
        """Represents a Composite as {attr1: str(attr1), attr2: str(attr2), ...}"""
        string = '{'
        for key in self.__ordered__:
            string += '{}: {}, '.format(key, self.__dict__[key])
        string = string[:-1]
        string += '}'
        return string

    def __setattr__(self, key, value):
        """
        Catches all attribute settings to Serializable types

        Only allows the setting if the attribute being set has a 'set' method. If it does
        it calls attribute.set(value). Otherwise setting is disallowed on the attribute.
        """
        if key in self.__ordered__:
            serializable = self.__dict__[key]
            if not callable(getattr(serializable, 'set', None)):
                raise ValueError("Cannot assign directly to '{}' ({})".format(key, type(serializable)))
            serializable.set(value)
        else:
            Serializable.__setattr__(self, key, value)

    def __getattribute__(self, item):
        """
        Catches all attribute getting to Serializable types.

        If the attribute defines a 'get' method it returns that instead, otherwise it just returns the attribute.
        """
        get_attribute = lambda item: Serializable.__getattribute__(self, item)
        _dict = get_attribute('__dict__')
        if item not in type(self).__ordered__:
            return get_attribute(item)
        serializable = _dict[item]
        return serializable.get() if callable(getattr(serializable, 'get', None)) else serializable

    def set(self, other):
        """
        Sets each Serializable attribute of Composite with the attributes of another of the same Composite.

        Args:
            other: The other Composite to set from.
        """
        if type(other) != type(self):
            raise ValueError("Types do not match: '{}' != '{}'".format(type(other), type(self)))
        for serializable in other.__ordered__:
            self.__setattr__(serializable, other.__getattribute__(serializable))

    def load_in_place(self, data, index=0):
        """Recursively calls load_in_place on each Serializable attribute."""
        for key in self.__ordered__:
            index = self.__dict__[key].load_in_place(data, index)
        return index

    def to_bytes(self):
        """Recursively calls to_bytes on each Serializable attribute"""
        data = bytearray()
        for key in self.__ordered__:
            data += self.__dict__[key].to_bytes()
        return data
