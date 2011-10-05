from PyQt4.QtCore import QSize
from PyQt4.QtGui import QTreeWidgetItem, QTreeWidget, QIcon, QSizePolicy
from models import StructuredNode

__author__ = 'darvin'

import rc


class SchemeTreeWidget(QTreeWidget):
    __icons_cache = {}
    def __init__(self, scheme, parent=None):
        super(SchemeTreeWidget, self).__init__(parent)
        self.load(scheme)
        self.setColumnCount(3)
#        self.header().hide()
        self.setHeaderLabels(("Name", "Type", "Description"))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def set_scheme(self, scheme):
        self.scheme = scheme

    def sizeHint(self):
        s = self.size()
        return QSize(s.width()+20, s.height())
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


    def load(self, scheme):
        self.clean()
        self.scheme = scheme
        self.__load(self.scheme, self)
        self.resizeColumnToContents(0)
        self.resizeColumnToContents(1)
        self.resizeColumnToContents(2)

