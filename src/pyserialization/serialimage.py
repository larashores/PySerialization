from pyserialization.serializable import Serializable
from pyserialization.serialint import SerialU32

import io

from PIL import Image



class SerialImage(Serializable):
    """
    A Saveable image type that can hold PIL images
    """
    def __init__(self, image=Image.new('RGB', (1, 1))):
        """
        Initializes the SerialImage with a given image or a null image
        """
        self.set(image)

    def get(self):
        """
        Returns the image object
        """
        return self._image

    def set(self, value):
        """
        Sets the value of the image
        """
        if value is not None and not isinstance(value, Image.Image):
            raise ValueError('{} is not an image type'.format(value))
        self._image = value

    def load_in_place(self, data, index=0):
        """Loads the image size as a U32 and then the data using the PIL library"""
        size, index = SerialU32.from_bytes(data, index)
        end_index = index + size.get()
        image_data = data[index:end_index]
        with io.BytesIO(image_data) as stream:
            stream.seek(index)
            self._image = Image.open(stream)
            self._image.load()
        return end_index

    def to_bytes(self):
        """Saves the image by saving its size as a U32 and then the data using the PIL library"""
        stream = io.BytesIO()
        self._image.save(stream, format=self._image.format if self._image.format is not None else 'PNG')
        size = SerialU32(len(stream.getvalue()))
        return size.to_bytes() + stream.getvalue()
