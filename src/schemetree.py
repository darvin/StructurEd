from PyQt4.QtGui import QTreeWidgetItem, QTreeWidget
from models import StructuredNode

__author__ = 'darvin'




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

