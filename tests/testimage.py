import unittest

try:
    from PIL import Image
    pil_installed = True
except ImportError:
    pil_installed = False

if pil_installed:
    from pyserialization.serialimage import SerialImage


@unittest.skipIf(not pil_installed, 'PIL not installed')
class TestSerialImage(unittest.TestCase):
    def test_default(self):
        image1 = SerialImage()
        image2 = SerialImage.from_bytes(image1.to_bytes())[0]
        self.assertEqual(image2.get().size, (1, 1))

    def test_red(self):
        image1 = SerialImage(Image.new('RGB', (100, 100), color='red'))
        image2 = SerialImage.from_bytes(image1.to_bytes())[0]
        self.assertEqual(image2.get().size, (100, 100))
        for i in range(100):
            for j in range(100):
                r, g, b = image2.get().getpixel((i, j))
                self.assertEqual(r, 255)
                self.assertEqual(g, 0)
                self.assertEqual(b, 0)