from PyQt4.QtCore import Qt
from PyQt4.QtGui import QToolBar, QMainWindow, QToolButton, QMessageBox, QStackedWidget, QStatusBar
import os
from models import Path, StructuredNode
from widgets import StructuredWidget


class LabelPath(QToolButton):

    def __init__(self, open_func, parent=None):
        super(LabelPath, self).__init__(parent)
        self.path = None
        self.open_func = open_func
        self.clicked.connect(self.openPath)
#        self.setFlat(True)

    def setPath(self, path):
        self.path = path
        if path:
            self.setText(path[-1])
        else:
            self.setText("/")

    def openPath(self):
        self.open_func(self.path)


class PathWidget(QStatusBar):

    MAX_PATH_LENGTH = 30 #fixme
    def __init__(self, open_func, path=None, parent=None):
        super(PathWidget, self).__init__(parent)
        if not path:
            path = Path(())

        self._labels = []

        for i in range(self.MAX_PATH_LENGTH):
            nameLabel = LabelPath(open_func, self)
            self._labels.append(nameLabel)
            self.addWidget(nameLabel)
            nameLabel.hide()

        self.setPath(path)

    def setPath(self, path):
        self.path = path
        for i in range(len(path)+1):
            self._labels[i].setPath(Path(path[:i]))
            self._labels[i].show()
        for j in range(len(path)+1, self.MAX_PATH_LENGTH):
            self._labels[j].hide()

class NodeWindow(QMainWindow):
    def __init__(self, data, scheme, parent=None):
        super(NodeWindow, self).__init__(parent)
        self.pathWidget = PathWidget(self.openWidgetByPath, data.path())
        self.setStatusBar(self.pathWidget)
#        layout_set_sm_and_mrg(self.layout)
        self.cachedWidgets = {}
        self.currentStructuredWidget = None
        self.stacked = QStackedWidget(self)
        self.setCentralWidget(self.stacked)

        self.data, self.scheme = data, scheme
        self.data.add_set_notify(self.change_caption)
        self.openWidgetByPath(Path())
        self.toolbar = QToolBar()
        self.toolbar.addActions((self.parent().actionSave,self.parent().actionSaveAs, ))
        self.addToolBar(self.toolbar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.messageBoxChanged = None
        self.reallyQuit = False
        self.change_caption()

    def change_caption(self):
        changed = ""
        if self.data.changed:
            changed = "* "
        self.setWindowTitle("{} {}".format(changed, self.get_window_caption()))

    def get_window_caption(self):
        return os.path.basename(self.parent().save_filename)


    def openWidgetByPath(self, path):
        if path in self.cachedWidgets:
#            if self.currentStructuredWidget:
#                self.currentStructuredWidget.hide()
            self.currentStructuredWidget = self.cachedWidgets[path]
            self.stacked.setCurrentWidget(self.currentStructuredWidget)
            self.pathWidget.setPath(path)
        else:
            if "Type" not in path.get(self.scheme): #fimxe soon
                self.cachedWidgets[path] = StructuredWidget(unicode(path), path.get(self.data), path.get(self.scheme), self.openWidgetByPath, self)
                self.stacked.addWidget(self.cachedWidgets[path])
                self.openWidgetByPath(path)
            else:
                pass

    def closeEvent(self, event):
        if self.reallyQuit or not self.data.changed:
            event.accept()
        else:
            self.dialogChanged()
            event.ignore()

    def dialogChanged(self):
        if not self.messageBoxChanged:
            self.messageBoxChanged = QMessageBox("SDI",
                "The document has been modified.\n"+
                    "Do you want to save your changes?",
                QMessageBox.Warning,
                QMessageBox.Yes | QMessageBox.Default,
                QMessageBox.No,
                QMessageBox.Cancel | QMessageBox.Escape,
                self
            )
            self.messageBoxChanged.setWindowModality (Qt.WindowModal )
            self.messageBoxChanged.finished.connect(self.finishClose)
        self.messageBoxChanged.show()

    def finishClose(self, value):
        if value==QMessageBox.Yes:
            self.reallyQuit = self.parent().save_data()
            if not self.reallyQuit:
                return
        elif value==QMessageBox.No:
            self.reallyQuit = True
        elif value==QMessageBox.Cancel:
            return
        self.close()
