import enum


class Endianess(enum.Enum):
    """Enumerates the possible endianess' for the struct module and the character used to represent it"""
    native = '='
    little = '<'
    big = '>'
