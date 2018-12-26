from abc import abstractmethod, ABCMeta


class Serializable(metaclass=ABCMeta):
    """
    A Serializable type is a type that can be converted to and from a bytes object.

    Each type must define it's own to_bytes and from_bytes methods. As each type clearly defines how it is stored,
    in contrast to storing data with pickle, the data should be compact, easily loadable, and easily interpreted from
    other programming languages.
    """

    @classmethod
    def from_bytes(cls, data, index=0, **kwargs):
        """
        Returns a new Serializable object from a bytearray

        Args:
            byte_array: The bytearray representing the object
            index:      The index in the bytearray where the data starts
        """
        obj = cls(**kwargs)
        index = obj.load_in_place(data, index)
        return obj, index

    @abstractmethod
    def to_bytes(self):
        """Return a bytearray representation of the Serializable"""
        return bytes()

    @abstractmethod
    def load_in_place(self, data, index=0):
        """
        Takes an existing Serializable and updates it such that it is equivalent to its bytearray representation

        Args:
            byte_array: The bytearray representing the object
            index:      The index in the bytearray where the data starts
        """
        return index

    def copy(self):
        """Copies a Serializable by creating a new Serializable from the old's bytearray representation"""
        new = type(self)()
        new.load_in_place(self.to_bytes())
        return new
