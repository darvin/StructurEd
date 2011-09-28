from PyQt4 import Qt
import os
from models import StructuredNode
from nodewindow import NodeWindow
from schemetree import SchemeTreeWidget
from src.utils import merge_dictionary

__author__ = 'darvin'
import plistlib



import sys
from PyQt4.QtGui import *

from PyQt4.QtCore import QSettings
import rc


class MainWindow(QMainWindow):
    def __init__(self, fixed_data_filename=None, fixed_scheme_filename=None):
        super(MainWindow, self).__init__()
        self.settings = QSettings()

        self.save_filename = None
        self.scheme_filename = None
        self.globalMenuBar = QMenuBar()

        menuFile = self.globalMenuBar.addMenu("File")
        self.toolbar = QToolBar()

        self._scheme = StructuredNode({})
        self._data = StructuredNode({})

        if not fixed_scheme_filename:
            actionLoadScheme = QAction(QIcon(":/icons/scheme-open.png"), "Load scheme file", self)
            actionLoadScheme.triggered.connect(self.load_scheme)
            menuFile.addActions((actionLoadScheme, ))
            self.toolbar.addActions((actionLoadScheme, ))


        if not fixed_data_filename:
            actionOpen = QAction(QIcon(":/icons/document-open.png"), "Open", self)
            actionOpen.triggered.connect(self.load_data)
            menuFile.addActions((actionOpen, ))
            self.toolbar.addActions((actionOpen, ))


        self.actionSave = actionSave = QAction(QIcon(":/icons/document-save.png"),"Save", self)
        actionSave.triggered.connect(self.save_data)
        self.actionSaveAs = actionSaveAs = QAction(QIcon(":/icons/document-save-as.png"),"Save as...", self)
        actionSaveAs.triggered.connect(self.save_data_as)

        self.actionMerge = QAction("Merge", self)
        self.actionMerge.triggered.connect(self.merge_data)


#        actionOpenRoot = QAction(QIcon(":/icons/window-new.png"), "Open root item", self)
#        actionOpenRoot.triggered.connect(self._open_root)

        menuFile.addActions((actionSave, actionSaveAs, self.actionMerge))
        self.toolbar.addActions((self.actionMerge,))



        self.addToolBar(self.toolbar)
        self.setUnifiedTitleAndToolBarOnMac(True)


        self.scheme_tree_view = SchemeTreeWidget(self._scheme)
        self.scheme_tree_view.load(self._scheme)
        self.setCentralWidget(self.scheme_tree_view)

        self.node_window = None

        try:
            self._read_settings(fixed_scheme_filename, fixed_data_filename)
        except IOError:
            pass


    def _read_settings(self, fixed_scheme_filename=None, fixed_data_filename=None):
        scheme_filename = fixed_scheme_filename or unicode(self.settings.value('recent_files/scheme').toString())
        if scheme_filename:
            self.__load_scheme(scheme_filename)
        data_filename = fixed_data_filename or unicode(self.settings.value('recent_files/data').toString())
        if data_filename:
            self.__load_data(data_filename)

    def _write_settings(self):
        self.settings.setValue('recent_files/data', self.save_filename)
        self.settings.setValue('recent_files/scheme', self.scheme_filename)

    def _open_root(self):
        if self.node_window:
            self.node_window.close()
        self.node_window = NodeWindow(self._data, self._scheme, parent=self)
        self.node_window.show()

    def closeEvent(self, event):
        self._write_settings()
        if self.dialogChanged():
            event.accept()
        else:
            event.reject()

    def dialogChanged(self):
        return True


    def save_data(self):
        if self.save_filename:
            dump = self._data.dump()
            plistlib.writePlist(dump, unicode(self.save_filename))
            return True
        else:
            return self.save_data_as()

    def save_data_as(self):

        self.save_filename = unicode(QFileDialog.getSaveFileName(self, "Save File",
                            "New Structured Property List.plist",
                            "Property Lists (*.plist)"))
        if self.save_filename:
            return self.save_data()


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


    def merge_data(self):
        add_data_filename = unicode(QFileDialog.getOpenFileName(self, "Open File",
#                            "sample_data.plist",
                            "Property Lists (*.plist)"))

        self._data = StructuredNode(merge_dictionary(self._data.dump(), plistlib.readPlist(add_data_filename)))
        self._open_root()


    def __load_scheme(self, scheme_filename):
        self._scheme = StructuredNode(plistlib.readPlist(scheme_filename))
        self.scheme_filename = scheme_filename
        self.scheme_tree_view.load(self._scheme)
        self.adjustSize()

    def __load_data(self, data_filename):
        self._data = StructuredNode(plistlib.readPlist(data_filename))
        self.save_filename = data_filename
        self._open_root()

    def _load_data_and_scheme(self, data_filename, scheme_filename):
        self.__load_scheme(scheme_filename)
        self.__load_data(data_filename)


