from copy import deepcopy
from models import StructuredNode, Path, ArrayNode, NumberNode, StringNode

__author__ = 'darvin'
import plistlib

scheme_filename = "/Users/darvin/Workspace/flipper/editor/sample_scheme.plist"

scheme = plistlib.readPlist(scheme_filename)

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import Qt


DEFAULT_VALUES = {
    "StructuredDictionary": lambda: StructuredNode({}),
    "Filename":lambda: StringNode(""),
    "String":lambda: StringNode(""),
    "Number":lambda: NumberNode(0),
    "Array":lambda: ArrayNode(()),

}

DATA = {"Ships":{"Ship1":{},"Ship2":{}}, "Parts":{"part1":{}, "part2":{}}}

def get_or_create_dict_element(dictionary, key, default_value):
    if key in dictionary:
        return dictionary[key]
    else:
        dictionary[key] = default_value
        return dictionary[key]

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
    def add_node_widget(cls, widget_class):
        cls.__node_widgets_classes[widget_class.data_type] = widget_class

    @classmethod
    def create_node_widget(cls, name, data, scheme, **kwargs):
        return cls.__node_widgets_classes[scheme["Type"].get()](name, data, scheme, **kwargs)


class StringWidget(QLineEdit, NodeWidget):
    data_type = "String"
    def __init__(self, name, data, scheme, parent=None):
        QLineEdit.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.editingFinished.connect(self.dump)
    def load(self):
        self.setText(unicode(self.data.get()))

    def dump(self):
        self.data.set(unicode(self.text()))

NodeWidget.add_node_widget(StringWidget)

class FilenameWidget(StringWidget):
    data_type = "Filename"
NodeWidget.add_node_widget(FilenameWidget)


class NumberWidget(QSpinBox, NodeWidget):
    data_type = "Number"
    def __init__(self, name, data, scheme, parent=None):
        QSpinBox.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.editingFinished.connect(self.dump)
    def load(self):
        self.setValue(self.data.get())

    def dump(self):
        self.data.set(self.value())
NodeWidget.add_node_widget(NumberWidget)




class ArrayWidget(QtGui.QWidget, NodeWidget):
    data_type = "Array"
    two_rows = True
    def __init__(self, name, data, scheme, parent=None):
        QtGui.QWidget.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._listwidget = QListWidget(self)
        self.layout.addWidget(self._listwidget)
        hlayout = QHBoxLayout(self)
        self.layout.addLayout(hlayout)
        self._add_button = QPushButton("add", self)
        hlayout.addWidget(self._add_button)
        self._add_button.clicked.connect(self.add_item)


        self._delete_button = QPushButton("del", self)
        hlayout.addWidget(self._delete_button)
        self._delete_button.clicked.connect(self.delete_item)



        self.element_scheme = self.scheme["ElementScheme"]
        self.new_data = DEFAULT_VALUES[self.element_scheme["Type"].get()]()
        self.add_widget = NodeWidget.create_node_widget("__not_exist", self.new_data, self.element_scheme)
        hlayout.addWidget(self.add_widget)




    def delete_item(self):
        row = self._listwidget.row(self._listwidget.currentItem())
        new_data = list(self.data.get())
        del new_data[row]
        self.data.set(tuple(new_data))
        self.load()

    def add_item(self):
        self.data.set(self.data.get()+(self.new_data.get(),))
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
NodeWidget.add_node_widget(ArrayWidget)


class StructuredWidget(QtGui.QWidget, NodeWidget):
    def __init__(self, name, data, scheme, open_func, parent=None):
        QtGui.QWidget.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle(self.name)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.open = open_func

        i = 0
        for child_name, child_scheme in self.scheme.iteritems():
            widget = NodeWidget.create_node_widget(child_name, get_or_create_dict_element(self.data, child_name, DEFAULT_VALUES[child_scheme["Type"].get()]()), child_scheme, parent=self)
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




class StructuredDictionaryWidget(QtGui.QWidget, NodeWidget):
    data_type = "StructuredDictionary"
    two_rows = True
    def __init__(self, name, data, scheme, parent=None):
        QtGui.QWidget.__init__(self, parent)
        NodeWidget.__init__(self, name, data, scheme)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self._listwidget = QListWidget(self)
        self.layout.addWidget(self._listwidget)
        hlayout = QHBoxLayout(self)
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
        self.parent().open(self.data.path()+(name,))

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
NodeWidget.add_node_widget(StructuredDictionaryWidget)



class SchemeTreeWidget(QTreeWidget):
    def __init__(self, scheme, parent=None):
        super(SchemeTreeWidget, self).__init__(parent)
        self.scheme = scheme
        self.setColumnCount(3)
#        self.header().hide()
        self.setHeaderLabels(("Name", "Type", "Description"))

    def _create_item_from_node(self, node, parent):
        if "Type" in node:
            type = node["Type"].get()
        else:
            type = ""

        if "Description" in node:
            desc = node["Description"].get()
        else:
            desc = ""

        item = QTreeWidgetItem(parent, [node.name, type, desc ])
        item.setExpanded(True)
        return item

    def __load(self, node, parent_item):
        for n_name, n in node.iteritems():
            if n.__class__==StructuredNode:
                item = self._create_item_from_node(n, parent_item)
                self.__load(n, item)

    def load(self, scheme):
        self.scheme = scheme
        self.__load(self.scheme, self)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.save_filename = None
        self.globalMenuBar = QMenuBar()
        actionLoadScheme = QAction(self.style().standardIcon(QStyle.SP_FileIcon), "Load scheme file", self)
        actionLoadScheme.triggered.connect(self.load_scheme)
        actionSave = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton),"Save", self)
        actionSave.triggered.connect(self.save_data)
        actionOpen = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), "Open", self)
        actionOpen.triggered.connect(self.load_data)
        actionSaveAs = QAction(self.style().standardIcon(QStyle.SP_DialogSaveButton),"Save as...", self)
        actionSaveAs.triggered.connect(self.save_data_as)


        actionOpenRoot = QAction(self.style().standardIcon(QStyle.SP_DirHomeIcon), "Open root item", self)
        actionOpenRoot.triggered.connect(self._open_root)


        menuFile = self.globalMenuBar.addMenu("File")
        menuFile.addActions((actionLoadScheme, actionOpen, actionSave, actionSaveAs))
        self.cachedWindows = {}


        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.toolbar.addActions((actionLoadScheme, actionOpen, actionSave, actionOpenRoot))

        self.__data = StructuredNode({})
        self.__scheme = {}

        self.scheme_tree_view = SchemeTreeWidget(self.__scheme)
        self.scheme_tree_view.load(self.__scheme)
        self.setCentralWidget(self.scheme_tree_view)

    def _open_root(self):
        self.open_window(())

    def open_window(self, path):
        if path in self.cachedWindows:
            self.cachedWindows[path].show()
        else:
            p = Path(path)
            self.cachedWindows[path] = StructuredWidget(unicode(p), p.get(self.__data), p.get(self.__scheme), open_func=self.open_window)
            self.open_window(path)



    def save_data(self):
        if self.save_filename:
            dump = self.__data.dump()
            plistlib.writePlist(dump, unicode(self.save_filename))
        else:
            self.save_data_as()

    def save_data_as(self):

        self.save_filename = unicode(QFileDialog.getSaveFileName(self, "Save File",
                            "newpropetylist.plist",
                            "Property Lists (*.plist)"))
        if self.save_filename:
            self.save()


    def load_data(self):
        self.save_filename = unicode(QFileDialog.getOpenFileName(self, "Open File",
#                            "newpropetylist.plist",
                            "Property Lists (*.plist)"))
        if self.save_filename:
            self.__load_data(StructuredNode(plistlib.readPlist(self.save_filename)))


    def load_scheme(self):
        self.scheme_name = unicode(QFileDialog.getOpenFileName(self, "Open File",
#                            "newpropetylist.plist",
                            "Property Lists (*.plist)"))
        if self.scheme_name:
            self.__load_scheme(StructuredNode(plistlib.readPlist(self.scheme_name)))



    def __load_scheme(self, scheme):
        self.__scheme = scheme
        self.scheme_tree_view.load(self.__scheme)

    def __load_data(self, data):
        self.__data = data
        
app = QtGui.QApplication(sys.argv)
#qb = StructuredWidget("root", DATA, scheme)
mainwindow = MainWindow()

mainwindow.show()
sys.exit(app.exec_())