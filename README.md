# PySerialization
Set of classes allowing easy serialization of simple and composite types.

The Python `pickle` module can flexibly serialize and deserialize most Python data types. However, due to it's flexibility, it is not just as trivial to interpret these files without the `pickle` module, such as in another programming language. Additionally, `pickle` has it's limitations on what can be serialized, and anything created with the `pyserialization` module is gaurenteed to serialize.

This module includes classes that explicitly define their serialization/deserialization procedure. They are stored as compactly as possible without extra meta data, as type information is stored in the classes themselves. Concrete classes are provided for basic types and base classes provided to easily create new serializable types made with existing types. All types inherit from `Serializable`

The provided concrete types are:
 - `SerialInt` family
 - `SerialHalf`/`SerialFloat`/`SerialDouble`
 - `SerialChar`
 - `SerialString/SerialAsciiString`
 
The provided base types are:
 - `SerialList`
 - `SerialEnum`
 - `Composite`
 - `Union`
 
Optionally the following concret types are provided with additional modules
 - `SerialNdArray` (`numpy`)
 - `SerialImage` (`PIL`)
  
Serialization is performed through the method `data = serializable.to_bytes()`. This will return a python `bytes` object that can be later deserialized. An object is deserialized through `obj, index = SerializableType.from_bytes(data)`. This returns the deserialized object along with the index of the end of the data. Alternativly, an existing Serializable can be reset with `index = SerializableType.load_in_place(data)`. This just returns the index of the end of the data.

Most types mutable and can be set using a `SerialType.set()` method and the underlaying data can be accessed using the `SerialType.get()` method.
 
The concrete types are serialized compactly using the python `struct` module. The optional types are serialized using their respective modules. The base types are used to create new concrete types using existing serializable types. They work as follows:

### SerialList
A homogenious python list that can be serialized. A new SerialList type is creating by calling `serial_list(SerialType)`. For example:

    class IntList(serial_list(SerialU16)):
        pass

This will create a new list type that can hold U16 integers

### SerialEnum
Used to store a selected enum of a Python enum.Enum class. Example:

    class Color(enum.Enum):
        RED = 'red'
        BLUE = 'blue'
        GREEN = 'green'
    
    class SerialColor(serial_enum(Color0):
        pass
        
    color1 = SerialColor(Color.BLUE)
    color2 = SerialColor.from_bytes(color1.to_bytes())[0]
    
    # color2.get() == 'Color.BLUE'
    # Color2.get().value == 'blue'
    
### Composite
Possibly the most used base type. Used to create a new Serializable type that is a composite of multiple other existing types. All types will be serialized and deserialized as a unit. Assigning to composite subtype will call that types `set` method if it exists. If the subtype has a `get` method, retrieving that type will return `type.get()` instead.The composite types are specified as class attributes. Example:

    class Test(Composite):
        a = SerialU16
        b = SerialString
        c = SerialDouble
        
    composite1 = Test()
    composite1.a = 42             # Calls SerialU16.set(42)
    composite1.b = 'hello world'
    composite1.c = 3.4
    
    composite2 = Test.from_bytes(composite1.to_bytes())[0]
    
    # composite2.a == 42          # Calls SerialU16.get()
    # composite2.b == 'hello world'
    # composite2.c == 3.4
    
### Union
Will save anyone one of a number of Serializable types. Can only have the value of one type at a time and knows what type to recover. Can change the type using `Union.set`. Can use attribute setting if the subtype has a `set` method. Using attribute getting will return `subtype.get()` if the subtype has a `get` method. Example

    class Test(Union):
        a = SerialU16
        b = SerialString
        c = SerialDouble
        
    union1 = Test()
    union1.a = 42             # union1.get() == SerialU16(42)
    union1.b = 'hello world'  # union1.get() == SerialString('hello world')
    # print(union1.a) -> ValueError
    
    union2 = Test.from_bytes(union1.to_bytes())[0]
    
    # composite2.b == 'hello world'   # Calls SerialU16.get()
    # composite2.get() == 'SerialSting('hello world')
