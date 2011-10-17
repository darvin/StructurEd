from PyQt4.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QTreeWidgetItem, QVBoxLayout, QHBoxLayout, QTreeWidget, QIcon, QSizePolicy, QWidget
from models import StructuredNode, Path
from utils import PlusMinusWidget, TreeWidgetIter

__author__ = 'darvin'

import rc



class SchemeTreeEditorWidget(QWidget):
    def __init__(self, scheme, parent=None):
        super(SchemeTreeEditorWidget, self).__init__(parent)
        self._scheme_tree = SchemeTreeWidget(scheme)


        self.layout = QVBoxLayout(self)
#        self.layout.setMargin(0)
        self.layout.setContentsMargins(3,3,3,3)
        self.layout.addWidget(self._scheme_tree)

        hlayout = QHBoxLayout()
        self.layout.addLayout(hlayout)

        self._plus_minus_widget = PlusMinusWidget(self.create_item, self.delete_item, self)
        hlayout.addWidget(self._plus_minus_widget)

    def load(self, scheme):
        self._scheme_tree.load_new_scheme(scheme)

    def create_item(self):
        pass

    def delete_item(self):
        self._scheme_tree.delete_current()


class AbstractTreeWidget(QTreeWidget):
    __icons_cache = {}
    expanded_at_start = True
    def __init__(self, scheme, parent=None):
        super(AbstractTreeWidget, self).__init__(parent)
        self.load_new_scheme(scheme)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.itemSelectionChanged.connect(self._item_selection_changed)


    def sizeHint(self):
        s = self.size()
        return QSize(s.width()+40, s.height()+40)
    def _create_item_from_node(self, node, parent):
        if "Type" in node:
            type = node["Type"].get()
        else:
            type = ""

        if "Description" in node:
            desc = node["Description"].get()
        else:
            desc = ""

        item = QTreeWidgetItem(parent, [node.name, type, desc])
        item.node = node
        item.setExpanded(self.expanded_at_start)
        if type not in self.__icons_cache:
            self.__icons_cache[type] = QIcon(":/icons/small/datatypes/{}.png".format(type))
        item.setIcon(0, self.__icons_cache[type])
        return item

    def __load(self, node, parent_item):
        for n_name, n in node.iteritems():
            if n.__class__==StructuredNode:
                item = self._create_item_from_node(n, parent_item)
                self.__load(n, item)

    def clean(self):

        while self.topLevelItemCount():
            self.takeTopLevelItem(0)


    def load_new_scheme(self, scheme):
        self.scheme = scheme
        self.scheme.add_set_notify(self.load)
        self.load()



    def load(self):
        self.clean()
        self.__load(self.scheme, self)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)



    def delete_current(self):
        selected =  self.selectedItems()
        if selected:
            selected[0].node.delete_from_parent()

    pathChanged = pyqtSignal(Path)

    def _item_selection_changed(self):
        items = self.selectedItems()
        if items:
            item = items[0]
            path = item.node.path()
            self.pathChanged.emit(path)

    @pyqtSlot(Path)
    def pathChange(self, path):
        iterator = TreeWidgetIter(self)
        for item in iterator:
            if item.node.path()==path:
                self.setCurrentItem(item)




class SchemeTreeWidget(AbstractTreeWidget):
    def __init__(self, data, parent=None):
        super(SchemeTreeWidget, self).__init__(data, parent)
        self.setColumnCount(3)
#        self.header().hide()
        self.setHeaderLabels(("Name", "Type", "Description"))


class DataTreeWidget(AbstractTreeWidget):
    expanded_at_start = False
    def __init__(self, data, parent=None):
        super(DataTreeWidget, self).__init__(data, parent)
        self.header().hide()
