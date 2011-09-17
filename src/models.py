from operator import getitem

__author__ = 'darvin'

class Path(tuple):
    @classmethod
    def from_string(cls, path_str):
        return cls(path_str.split("/"))


    def get(self, root_node):
        effective_path = self
        if not root_node.is_root():
            for node_name in root_node.path():
                if effective_path[0]==node_name:
                    effective_path = effective_path[1:]
        current_node = root_node
        for name in effective_path:
            if name in current_node:
                current_node = current_node[name]
            elif "ElementStructure" in current_node:
                current_node = current_node["ElementStructure"]
        return current_node

    def __unicode__(self):
        return "/".join(self)

    def __str__(self):
        return unicode(self)




class Node(object):
    def __init__(self, value, name=None, parent=None):
        self._value = value
        if not parent:
            self.name = "root"
        else:
            if not name:
                raise NotImplementedError
            self.name = name
        self.parent = parent

    def is_root(self):
        return self.parent is None

    def __unicode__(self):
        return unicode(self._value)

    def __str__(self):
        return str(self._value)

    def get(self):
        return self._value

    def dump(self):
        return self.get()

    def set(self, value):
        self._value = value

    def path(self):
        if not self.parent:
            return Path()
        else:
            return Path(self.parent.path()+(self.name,))

class TypedNode(Node):
    types = None

    def _check_type(self, value):
        if not isinstance(value, self.types):
            raise NotImplementedError

    def set(self, value):
        self._check_type(value)
        super(TypedNode, self).set(value)


class StringNode(TypedNode):
    types = (unicode, str)

class NumberNode(TypedNode):
    types = (int, float)

class ArrayNode(TypedNode):
    types = (list, tuple)

class DictNode(TypedNode):
    types = (dict,)

TYPED_NODE_CLASSES = (StringNode, NumberNode, ArrayNode, )

class StructuredNode(DictNode):
    def dump(self):
        result = {}
        for key, value in self._value.iteritems():
            result[key] = value.dump()
        return result

    def __init__(self, value, name=None, parent=None):
        super(StructuredNode, self).__init__({}, name, parent)
        for key, v in value.items():
            value_class = v.__class__ or v.__type__
            for node_class in TYPED_NODE_CLASSES+(self.__class__,):
                if issubclass(value_class, node_class.types):
                    self[key] = node_class(v)
                    break

    def _check_type_item(self, value):
        if not issubclass(value.__class__, Node):
            raise NotImplementedError

    def __getitem__(self, item):
        return self._value[item]

    def __iter__(self):
        return iter(self._value)

    def keys(self):
        return self._value.keys()

    def iteritems(self):
        return  self._value.iteritems()

    def __setitem__(self, key, value):
        self._check_type_item(value)
        value.name = key
        value.parent = self
        if key not in self._value:
            self._value[key] = value
        else:
            raise NotImplementedError

    def __delitem__(self, key):
        del self._value[key]

    def rename_item(self, old_name, new_name):
        if new_name in self._value:
            raise NotImplementedError
        self._value[new_name] = self._value[old_name]
        del self._value[old_name]
        self._value[new_name].name = new_name