from unitreeserializer import loads, dumps
import unittest
from unitreeserializer.format import Format

class TestUniTreeSerializerFunctions(unittest.TestCase):

    def setUp(self):
        self.some_data = {"dict1":{"dict1.1":{"somestr":"string", "somearray":[2,5,67,3]},"dict1.2":{"some float":6.7}},"dict2":{"dict2.1":{"dict2.1.1":{"number":3}}}}
        

    def test_sanity(self):
        print Format.get_formats()
        for format in Format.get_formats():
            st = dumps(self.some_data, format)
            print st
            self.assertTrue(isinstance(st, (unicode, str)))
            self.assertEqual(self.some_data, loads(st, format))

if __name__ == '__main__':
    unittest.main()