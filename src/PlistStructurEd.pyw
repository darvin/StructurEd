from copy import deepcopy
import os
from models import StructuredNode, Path, ArrayNode, NumberNode, StringNode
from nodewindow import NodeWindow
from schemetree import SchemeTreeWidget
from widgets import StructuredWidget

__author__ = 'darvin'
import plistlib

DEBUG = True

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *




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



        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.toolbar.addActions((actionLoadScheme, actionOpen, actionSave, actionOpenRoot))

        self.__data = StructuredNode({})
        self.__scheme = StructuredNode({})

        self.scheme_tree_view = SchemeTreeWidget(self.__scheme)
        self.scheme_tree_view.load(self.__scheme)
        self.setCentralWidget(self.scheme_tree_view)

    def _open_root(self):
        NodeWindow(self.__data, self.__scheme).show()




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

    def _load_data_and_scheme(self, data, scheme):
        self.__load_scheme(scheme)
        self.__load_data(data)


if __name__=="__main__":

    app = QtGui.QApplication(sys.argv)
    #qb = StructuredWidget("root", DATA, scheme)
    mainwindow = MainWindow()

    mainwindow.show()



    if DEBUG:
        scheme_filename = os.path.join(os.getcwd(), "..", "tests","test_data","sample_scheme.plist")

        scheme = StructuredNode(plistlib.readPlist(scheme_filename))
        data = StructuredNode({"Ships":{"Ship1":{},"Ship2":{}}, "Parts":{"part1":{}, "part2":{}}})
        mainwindow._load_data_and_scheme(data, scheme)



    sys.exit(app.exec_())