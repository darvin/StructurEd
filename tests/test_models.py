from models import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.root = StructuredNode({})
        child1 = StructuredNode({})
        child2 = StructuredNode({})
        self.root["child1"] = child1
        self.root["child2"]= child2
        int1 = NumberNode(3, "int1", child1)
        child1["int1"]=int1
        self.subchild1 = StructuredNode({})
        child2["subchild"] = self.subchild1
        self.str1 = StringNode("SomeValue")
        self.subchild1["str"] = self.str1

        self.some_data = {"dict1":{"dict1.1":{"somestr":"string", "somearray":[2,5,67,3]},"dict1.2":{"some float":6.7}},
                "dict2":{"dict2.1":{"dict2.1.1":{"number":3}}}}
        

    def test_path_sanity(self):
        path_str1 = self.str1.path()
        self.assertEqual(('child2', 'subchild', 'str'), path_str1)
        self.assertEqual(path_str1.get(self.root), self.str1)
        print

    def test_rename_item(self):
        self.root["child1"].rename_item("int1", "newint1")
        self.assertEqual(3, self.root["child1"]["newint1"].get())

    def test_flat_dict_conversions_sanity(self):
        stnode = StructuredNode(self.some_data)
        self.assertEqual(self.some_data, stnode.dump() )

    def test_flat_dict_conversions(self):
        stnode = StructuredNode(self.some_data)
        self.assertEqual("string",Path(("dict1", "dict1.1", 'somestr')).get(stnode).get())

if __name__ == '__main__':
    unittest.main()