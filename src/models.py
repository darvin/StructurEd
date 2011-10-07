from copy import deepcopy
from operator import getitem

__author__ = 'darvin'

META_KEY = "__META"

class Path(tuple):
    def __new__(cls, tupl=None, is_relative=False):
        if tupl is None:
            tupl = ()
        result = tuple.__new__(cls, tupl)
        result.is_relative = is_relative
        return result

    @classmethod
    def from_string(cls, path_str):
        return cls([name for name in path_str.split("/") if name], is_relative=not path_str.startswith("/"))


    def get(self, root_node, reduce_sub_elements=False):
        current_node = self._get_root_node(root_node)
        for name in self:
            if reduce_sub_elements and name=="SubElements":
                continue
            if name in current_node:
                current_node = current_node[name]
            elif "ElementStructure" in current_node:
                current_node = current_node["ElementStructure"]
            else:
                raise KeyError
        return current_node

    def set(self, root_node, value):
        current_node = self._get_root_node(root_node)
        print unicode(self), value
        for i, name in enumerate(self):
            if i<(len(self)-1):
                if name not in current_node:
                    current_node.create_structured_child(name)
                current_node = current_node[name]
            else:
                current_node[name] = value

    def __unicode__(self):
        if not self.is_relative:
            return "/"+"/".join(self)
        else:
            return "/".join(self)

    def __str__(self):
        return unicode(self)

    def _get_root_node(self, root_node):
        if not root_node.is_root() and not self.is_relative:
            return root_node.get_root()
        else:
            return root_node


class Node(object):
    __node_classes = {}
    def __init__(self, value, name=None, parent=None):
        self.changed = False
        self.initialized =False
        self.can_be_initalized = True
        self.__notify_at_set = []
        if not parent:
            self.name = "root"
        else:
            if not name:
                raise NotImplementedError
            self.name = name
        self.parent = parent
        self.set(value)

    def add_set_notify(self, func):
        self.__notify_at_set.append(func)

    def is_root(self):
        return self.parent is None

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        else:
            return self

    def get_meta(self):
        if META_KEY in self:
            return self._value[META_KEY]
        else:
            if not self.parent:
                return {}
            else:
                return self.parent.get_meta()

    def __unicode__(self):
        return unicode(self._value)

    def __str__(self):
        return str(self._value)

    def get(self):
        return self._value

    def dump(self):
        return self.get()

    def set_changed(self, changed, parents=False, children=False):
        self.changed = changed
        if parents:
            self.parent.set_changed(changed, parents)

    def _notify_set(self, not_notify=None):
        if self.initialized:
            self.changed = True

            if self.parent:
                self.parent._notify_set(not_notify)
        elif self.can_be_initalized:
            self.initialized=True
        for func in self.__notify_at_set:
            if func!=not_notify:
                func()

    def set(self, value, not_notify=None):
        self._value = value
        self._notify_set(not_notify)


    def delete_from_parent(self):
        del self.parent[self.name]

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
        try:
            return self.types[0](value)
        except ValueError:
            raise NotImplementedError

    def set(self, value, not_notify=None):
        value = self._check_type(value)
        super(TypedNode, self).set(value, not_notify)

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

    def set_changed(self, changed, parents=False, children=False):
        super(AbstractCollectionNode, self).set_changed(changed, parents)
        if children:
            self.map_subnodes(lambda node: node.set_changed(changed, parents, children))

    def map_subnodes(self, func):
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

    def create_structured_child(self, name):
        self[name] = self.__class__({}, name, self)
        return self[name]



    def _process_subnodes(self, value):
        self.can_be_initalized = False
        self.initialized = False
        for key, v in value.items():
            self[key] = Node.create_node(v)
        self.can_be_initalized = True
        self.initialized = True




    def keys(self):
        return self._value.keys()

    def iteritems(self):
        return ((key, value) for key, value in self._value.iteritems() if key!=META_KEY)

    def values(self):
        return self._value.values()

    def __setitem__(self, key, value):
        self._check_type_item(value)
        value.name = key
        value.parent = self
        if key not in self._value:
            self._value[key] = value
            self._notify_set()
        else:
            raise NotImplementedError

    def __delitem__(self, key):
        del self._value[key]
        self._notify_set()

    def rename_item(self, old_name, new_name):
        if new_name in self._value:
            raise NotImplementedError
        self._value[new_name] = self._value[old_name]
        del self._value[old_name]
        self._value[new_name].name = new_name

    def map_subnodes(self, func):
        for node in self._value.values():
            func(node)


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

    def values(self):
        return iter(self._value)


    def map_subnodes(self, func):
        for node in self._value:
            func(node)

    def _process_subnodes(self, value):
        for v in value:
            self._value.append(Node.create_node(v))
