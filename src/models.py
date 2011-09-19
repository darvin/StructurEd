from copy import deepcopy
from operator import getitem

__author__ = 'darvin'

class Path(tuple):
    @classmethod
    def from_string(cls, path_str):
        return cls([name for name in path_str.split("/") if name])


    def get(self, root_node):
        if not root_node.is_root():
            root_node = root_node.get_root()
        current_node = root_node
        for name in self:
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
    __node_classes = {}
    def __init__(self, value, name=None, parent=None):
        self._value = value
        self.__notify_at_set = []
        if not parent:
            self.name = "root"
        else:
            if not name:
                raise NotImplementedError
            self.name = name
        self.parent = parent

    def add_set_notify(self, func):
        self.__notify_at_set.append(func)

    def is_root(self):
        return self.parent is None

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        else:
            return self

    def __unicode__(self):
        return unicode(self._value)

    def __str__(self):
        return str(self._value)

    def get(self):
        return self._value

    def dump(self):
        return self.get()

    def _notify_set(self):
        for func in self.__notify_at_set:
            func()

    def set(self, value):
        self._notify_set()
        self._value = value

    def path(self):
        if not self.parent:
            return Path()
        else:
            return Path(self.parent.path()+(self.name,))

    @classmethod
    def register(cls, node_class):
        if not issubclass(node_class, cls):
            raise NotImplementedError
        cls.__node_classes[node_class.types] = node_class
        return node_class

    @classmethod
    def create_node(cls, value):
        value_class = value.__class__ or value.__type__
        for value_classes, node_class in cls.__node_classes.iteritems():
            if issubclass(value_class, value_classes):
               return node_class(value)

class TypedNode(Node):
    types = None

    def _check_type(self, value):
        if not isinstance(value, self.types):
            raise NotImplementedError

    def set(self, value):
        self._check_type(value)
        super(TypedNode, self).set(value)

@Node.register
class StringNode(TypedNode):
    types = (unicode, str)


@Node.register
class IntegerNode(TypedNode):
    types = (int, )


@Node.register
class RealNode(TypedNode):
    types = (float, )


@Node.register
class BooleanNode(TypedNode):
    types = (bool, )

class AbstractCollectionNode(TypedNode):
    types = None
    _default_value = None
    def __init__(self, value, name=None, parent=None):
        super(AbstractCollectionNode, self).__init__(deepcopy(self._default_value), name, parent)
        self._process_subnodes(value)

    def dump(self):
        raise NotImplementedError

    def _process_subnodes(self, value):
        raise NotImplementedError

    def __getitem__(self, item):
        return self._value[item]

    def __iter__(self):
        return iter(self._value)

    def _check_type_item(self, value):
        if not issubclass(value.__class__, Node):
            raise NotImplementedError


@Node.register
class StructuredNode(AbstractCollectionNode):
    types = (dict,)
    _default_value = {}
    def dump(self):
        result = {}
        for key, value in self._value.iteritems():
            result[key] = value.dump()
        return result



    def _process_subnodes(self, value):
        for key, v in value.items():
            self[key] = Node.create_node(v)




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


@Node.register
class ArrayNode(AbstractCollectionNode):
    types = (list, tuple)
    _default_value = []

    def __iter__(self):
        return iter(self._value)

    def __getitem__(self, item):
        return getitem(self._value, item)


    def dump(self):
        return [v.dump() for v in self._value]



    def _process_subnodes(self, value):
        for v in value:
            self._value.append(Node.create_node(v))
