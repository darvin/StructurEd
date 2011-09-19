import os
from models import StructuredNode
from nodewindow import NodeWindow
from schemetree import SchemeTreeWidget

__author__ = 'darvin'
import plistlib

DEBUG = True

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *

import rc


class MainWindow(QMainWindow):
    def __init__(self, fixed_data_filename=None, fixed_scheme_filename=None):
        super(MainWindow, self).__init__()
        self.settings = QSettings()

        self.save_filename = None
        self.globalMenuBar = QMenuBar()
        if not fixed_scheme_filename:
            actionLoadScheme = QAction(QIcon(":/icons/scheme-open.png"), "Load scheme file", self)
            actionLoadScheme.triggered.connect(self.load_scheme)
            self.__scheme = StructuredNode({})
        else:
            self.__load_scheme(fixed_scheme_filename)
        if not fixed_data_filename:
            actionSave = QAction(QIcon(":/icons/document-save.png"),"Save", self)
            actionSave.triggered.connect(self.save_data)
            actionOpen = QAction(QIcon(":/icons/document-open.png"), "Open", self)
            actionOpen.triggered.connect(self.load_data)
            actionSaveAs = QAction(QIcon(":/icons/document-save-as.png"),"Save as...", self)
            actionSaveAs.triggered.connect(self.save_data_as)
            self.__data = StructuredNode({})

        else:
            self.__load_data(fixed_data_filename)

        actionOpenRoot = QAction(QIcon(":/icons/window-new.png"), "Open root item", self)
        actionOpenRoot.triggered.connect(self._open_root)


        menuFile = self.globalMenuBar.addMenu("File")
        menuFile.addActions((actionLoadScheme, actionOpen, actionSave, actionSaveAs))



        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.toolbar.addActions((actionLoadScheme, actionOpen, actionSave, actionOpenRoot))


        self.scheme_tree_view = SchemeTreeWidget(self.__scheme)
        self.scheme_tree_view.load(self.__scheme)
        self.setCentralWidget(self.scheme_tree_view)

        self._read_settings()

    def _read_settings(self):
        scheme_filename = unicode(self.settings.value('recent_files/scheme').toString())
        if scheme_filename:
            self.__load_scheme(scheme_filename)
        data_filename = unicode(self.settings.value('recent_files/data').toString())
        if data_filename:
            self.__load_scheme(data_filename)

    def _write_settings(self):
        self.settings.setValue('recent_files/data', self.save_filename)
        self.settings.setValue('recent_files/scheme', self.scheme_filename)

    def _open_root(self):
        NodeWindow(self.__data, self.__scheme).show()

    def closeEvent(self, event):
        self._write_settings()
        event.accept()


    def save_data(self):
        if self.save_filename:
            dump = self.__data.dump()
            plistlib.writePlist(dump, unicode(self.save_filename))
        else:
            self.save_data_as()

    def save_data_as(self):

        self.save_filename = unicode(QFileDialog.getSaveFileName(self, "Save File",
                            "New Structured Property List.plist",
                            "Property Lists (*.plist)"))
        if self.save_filename:
            self.save_data()


    def load_data(self):
        data_filename = unicode(QFileDialog.getOpenFileName(self, "Open File",
#                            "sample_data.plist",
                            "Property Lists (*.plist)"))
        if data_filename:
            self.__load_data(data_filename)


    def load_scheme(self):
        scheme_filename = unicode(QFileDialog.getOpenFileName(self, "Open File",
#                            "sample_data.plist",
                            "Property Lists (*.plist)"))
        if scheme_filename:
            self.__load_scheme(scheme_filename)



    def __load_scheme(self, scheme_filename):
        self.__scheme = StructuredNode(plistlib.readPlist(scheme_filename))
        self.scheme_filename = scheme_filename
        self.scheme_tree_view.load(self.__scheme)
        self.adjustSize()

    def __load_data(self, data_filename):
        self.__data = StructuredNode(plistlib.readPlist(data_filename))
        self.save_filename = data_filename

    def _load_data_and_scheme(self, data_filename, scheme_filename):
        self.__load_scheme(scheme_filename)
        self.__load_data(data_filename)



if __name__=="__main__":

    app = QtGui.QApplication(sys.argv)

    app.setOrganizationName("SergeyKlimov")
    app.setOrganizationDomain("darvin.github.com")
    app.setApplicationName("StructurEd")
    mainwindow = MainWindow()

    mainwindow.show()

    if DEBUG:
        test_data_paths = (
            os.path.join(os.getcwd(), "..", "tests","test_data"),
            os.getcwd(),
        )
        for base_path in test_data_paths:
            scheme_filename = os.path.join(base_path, "sample_scheme.plist")
            data_filename = os.path.join(base_path, "sample_data.plist")
            if os.path.exists(scheme_filename) and os.path.exists(data_filename):
                mainwindow._load_data_and_scheme(data_filename, scheme_filename)



    sys.exit(app.exec_())