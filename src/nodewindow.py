from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QToolBar, QMainWindow, QToolButton, QMessageBox, QStackedWidget
from models import Path, StructuredNode
from utils import layout_set_sm_and_mrg, StyledButton
from widgets import StructuredWidget


class LabelPath(QToolButton):
    style = """
QPushButton {
    border: 1px solid #8B8B8B;
    border-radius: 0.4px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #F6F6F6, stop: 1 #DBDBDA);
    min-width: 35px;
    min-height: 20px;
}
QPushButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #dadbde, stop: 1 #f6f7fa);
}
        """

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


class PathWidget(QWidget):

    MAX_PATH_LENGTH = 30 #fixme
    def __init__(self, open_func, path=None, parent=None):
        super(PathWidget, self).__init__(parent)
        mainlayout = QHBoxLayout(self)
        self.layout = QHBoxLayout()
        mainlayout.addLayout(self.layout)
        mainlayout.addStretch(1)
        self.layout.setMargin(0)
#        self.layout.setSpacing(4)
        if not path:
            path = Path(())

        self._labels = []

        for i in range(self.MAX_PATH_LENGTH):
            nameLabel = LabelPath(open_func, self)
            self._labels.append(nameLabel)
            self.layout.addWidget(nameLabel)
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
        self.layout = QVBoxLayout(self)
        self.pathWidget = PathWidget(self.openWidgetByPath, data.path())
        self.statusBar().addWidget(self.pathWidget)
#        layout_set_sm_and_mrg(self.layout)
        self.cachedWidgets = {}
        self.currentStructuredWidget = None
        self.stacked = QStackedWidget(self)
        self.setCentralWidget(self.stacked)

        self.data, self.scheme = data, scheme
        self.openWidgetByPath(Path())
        self.toolbar = QToolBar()
        self.toolbar.addActions((self.parent().actionSave,self.parent().actionSaveAs, ))
        self.addToolBar(self.toolbar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.messageBoxChanged = None
        self.reallyQuit = False


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
        if self.reallyQuit:
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
