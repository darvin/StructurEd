from PyQt4.QtCore import Qt
from PyQt4.QtGui import QLineEdit, QSpinBox, QWidget, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QListWidgetItem, QGridLayout, QLabel, QAbstractItemView, QComboBox, QIntValidator, QDoubleValidator, QCheckBox
from models import StructuredNode, StringNode, IntegerNode, RealNode, BooleanNode, ArrayNode, Path, Node
from utils import get_or_create_dict_element




class NodeWidget(object):
    two_rows = False
    data_type = "NoSuchType"

    __node_widgets_classes = {}
    def __init__(self, name, data, scheme):

        self.data = data
        self.scheme = scheme
        self.name = name
        self.description =  name
        if "Description" in self.scheme:
            self.description = self.scheme["Description"].get()

    def load(self):
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError
#
#    def get_scheme(self):
#        return self.data.path().get(self.scheme)





    @classmethod
    def register(cls, widget_class): 
        if not issubclass(widget_class, cls):
            raise NotImplementedError
        cls.__node_widgets_classes[widget_class.data_type] = widget_class
        return widget_class

    @classmethod
    def create_node_widget(cls, name, data, scheme, **kwargs):
        return cls.__node_widgets_classes[scheme["Type"].get()](name, data, scheme, **kwargs)

    @classmethod
    def get_default_data(cls, scheme, data):
        new_data = cls.__node_widgets_classes[scheme["Type"].get()]._get_default_data(scheme, data)
        new_data.parent = data
        return new_data

    @classmethod
    def _get_default_data(self, scheme, data):
        raise NotImplementedError


@NodeWidget.register
class StringWidget(QLineEdit, NodeWidget):
    data_type = "String"
    def __init__(self, name, data, scheme, parent=None):
        QLineEdit.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.textEdited.connect(self.dump)
    def load(self):
        self.setText(unicode(self.data.get()))

    def dump(self):
        self.data.set(unicode(self.text()))

    @classmethod
    def _get_default_data(cls, scheme, data):
        return StringNode("")
@NodeWidget.register
class FilenameWidget(StringWidget):
    data_type = "Filename"


@NodeWidget.register
class IntegerWidget(StringWidget):
    data_type = "Integer"

    def __init__(self, name, data, scheme, parent=None):
        super(IntegerWidget, self).__init__(name, data, scheme, parent)
        validator = QIntValidator(self)
        self.setValidator(validator)

    def load(self):
        self.setText(unicode(self.data.get()))

    def dump(self):
        self.data.set(int(self.text()))

    @classmethod
    def _get_default_data(cls, scheme, data):
        return IntegerNode(0)

@NodeWidget.register
class RealWidget(StringWidget):
    data_type = "Real"
    def __init__(self, name, data, scheme, parent=None):
        super(RealWidget, self).__init__(name, data, scheme, parent)
        validator = QDoubleValidator(self)
        self.setValidator(validator)
        
    def load(self):
        self.setText(unicode(self.data.get()))

    def dump(self):
        self.data.set(float(self.text()))

    @classmethod
    def _get_default_data(cls, scheme, data):
        return RealNode(0.0)


@NodeWidget.register
class BooleanWidget(QCheckBox, NodeWidget):
    data_type = "Boolean"
    def __init__(self, name, data, scheme, parent=None):
        QCheckBox.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.stateChanged.connect(self.dump)
    def load(self):
        self.setChecked(self.data.get())

    def dump(self):
        self.data.set(self.isChecked())

    @classmethod
    def _get_default_data(cls, scheme, data):
        return BooleanNode(False)

@NodeWidget.register
class ArrayWidget(QWidget, NodeWidget):
    data_type = "Array"
    two_rows = True
    def __init__(self, name, data, scheme, parent=None):
        QWidget.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.layout = QVBoxLayout(self)
#        self.setLayout(self.layout)
        self._listwidget = QListWidget(self)
        self.layout.addWidget(self._listwidget)
        hlayout = QHBoxLayout()
        self.layout.addLayout(hlayout)
        self._add_button = QPushButton("add", self)
        hlayout.addWidget(self._add_button)
        self._add_button.clicked.connect(self.add_item)


        self._delete_button = QPushButton("del", self)
        hlayout.addWidget(self._delete_button)
        self._delete_button.clicked.connect(self.delete_item)



        self.element_scheme = self.scheme["ElementScheme"]
        self.new_data = NodeWidget.get_default_data(self.element_scheme, self.data)

        self.add_widget = NodeWidget.create_node_widget("__not_exist", self.new_data, self.element_scheme)
        hlayout.addWidget(self.add_widget)




    def delete_item(self):
        row = self._listwidget.row(self._listwidget.currentItem())
        new_data = list(self.data.get())
        del new_data[row]
        self.data.set(tuple(new_data))
        self.load()

    def add_item(self):
        self.data.set(list(self.data.get())+[Node.create_node(self.new_data.get()),])
        self.load()

    def __createItem(self, itemname):
        item = QListWidgetItem(itemname)
#        item.setFlags (Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )
        self._listwidget.addItem(item)





    def dump(self):
        pass

    def load(self):
        self._listwidget.clear()
        for item in self.data.get():
            self.__createItem(unicode(item))


    @classmethod
    def _get_default_data(cls, scheme, data):
        return ArrayNode([])

@NodeWidget.register
class StructuredWidget(QWidget, NodeWidget):
    def __init__(self, name, data, scheme, open_func, parent=None):
        QWidget.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle(self.name)
        self.layout = QGridLayout(self)
#        self.setLayout(self.layout)
        self.open = open_func

        i = 0
        for child_name, child_scheme in self.scheme.iteritems():
            widget = NodeWidget.create_node_widget(child_name, get_or_create_dict_element(self.data, child_name, NodeWidget.get_default_data(child_scheme, self.data)), child_scheme, parent=self)
            widget.load()
            if widget.two_rows:
                widget_col = 1
                widget_row = i+1
                widget_col_span = 2
                widget_row_span = 1
                label_col = 1
                label_row = i
                label_col_span = 2
                label_row_span = 1
                i+=1
            else:
                widget_col = 2
                widget_row = i
                widget_col_span = 1
                widget_row_span = 1
                label_col = 1
                label_row = i
                label_col_span = 1
                label_row_span = 1
            self.layout.addWidget(QLabel(widget.description, parent=self), label_row, label_col, label_row_span, label_col_span)
            self.layout.addWidget(widget, widget_row, widget_col, widget_row_span, widget_col_span)
            i+=1

    def load(self):
        pass


    @classmethod
    def _get_default_data(cls, scheme, data):
        return StructuredNode({})



@NodeWidget.register
class StructuredDictionaryWidget(QWidget, NodeWidget):
    data_type = "StructuredDictionary"
    two_rows = True
    def __init__(self, name, data, scheme, parent=None):
        QWidget.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.layout = QVBoxLayout(self)
#        self.setLayout(self.layout)
        self._listwidget = QListWidget(self)
        self.layout.addWidget(self._listwidget)
        hlayout = QHBoxLayout()
        self.layout.addLayout(hlayout)
        self._add_button = QPushButton("add", self)
        hlayout.addWidget(self._add_button)
        self._add_button.clicked.connect(self.create_item)


        self._edit_button = QPushButton("edit", self)
        hlayout.addWidget(self._edit_button)
        self._edit_button.clicked.connect(self.edit_item)

        self._delete_button = QPushButton("del", self)
        hlayout.addWidget(self._delete_button)
        self._delete_button.clicked.connect(self.delete_item)


        self._listwidget.setEditTriggers(QAbstractItemView.EditKeyPressed)
        self._listwidget.itemChanged.connect(self.rename_item)
        self._listwidget.currentItemChanged.connect(self.current_item_changed)
        self.current_item_index = None


    def edit_item(self):
        name = unicode(self._listwidget.currentItem().text())
        self.parent().open(Path(self.data.path()+(name,)))

    def delete_item(self):
        item_name = unicode(self._listwidget.currentItem().text())
        self._listwidget.takeItem(self._listwidget.row(self._listwidget.currentItem()))
        del self.data[item_name]

    def create_item(self):
        get_or_create_dict_element(self.data, "new item", StructuredNode({}))
        self.__createItem("new item")

    def __createItem(self, itemname):
        item = QListWidgetItem(itemname)

        item.setFlags (Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled )
        self._listwidget.addItem(item)

    def rename_item(self, item):
        self.data.rename_item(self.current_item_index, unicode(item.text()))
    def current_item_changed(self, item):
        self.current_item_index = unicode(item.text())




    def dump(self):
        pass

    def load(self):
        for key in self.data.keys():
            self.__createItem(key)

    @classmethod
    def _get_default_data(cls, scheme, data):
        return StructuredNode({})


@NodeWidget.register
class SelectWidget(QComboBox, NodeWidget):
    data_type = "Select"
    def __init__(self, name, data, scheme, parent=None):
        QComboBox.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)

        self._load_options()
        for i, option in enumerate(self.options):
            self.addItem(unicode(option), i)
        self.load()
        self.currentIndexChanged.connect(lambda index: self.dump())

    def _load_options(self):
        self.options = self.scheme["Options"]

    def load(self):
        for i, option in enumerate(self.options):
            if option.get()==self.data.get():
                self.setCurrentIndex(i)

    def dump(self):
        self.data.set(self.options[self.itemData(self.currentIndex()).toPyObject()].get())


    @classmethod
    def _get_default_data(cls, scheme, data):
        return Node.create_node(scheme["Options"][0].get())


@NodeWidget.register
class SelectObjectWidget(SelectWidget):
    data_type = "SelectObject"

    def _load_options(self):
        self.options = self._get_options_from_scheme(self.scheme, self.data)

    @classmethod
    def _get_options_from_scheme(cls, scheme, data):
        path = Path.from_string(scheme["OptionPath"].get())
        return [Node.create_node(name) for name in path.get(data).keys()]
        
    @classmethod
    def _get_default_data(cls, scheme, data):
        return cls._get_options_from_scheme(scheme, data)[0]
