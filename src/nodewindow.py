from PyQt4.QtGui import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton
from models import Path, StructuredNode
from utils import layout_set_sm_and_mrg, StyledButton
from widgets import StructuredWidget


class LabelPath(StyledButton):
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

class NodeWindow(QWidget):
    def __init__(self, data, scheme, parent=None):
        super(NodeWindow, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.pathWidget = PathWidget(self.openWidgetByPath, data.path())
        self.layout.addWidget(self.pathWidget)
        layout_set_sm_and_mrg(self.layout)
        self.cachedWidgets = {}
        self.currentStructuredWidget = None

        self.data, self.scheme = data, scheme
        self.openWidgetByPath(Path())

    def openWidgetByPath(self, path):
        if path in self.cachedWidgets:
            if self.currentStructuredWidget:
                self.currentStructuredWidget.hide()
            self.currentStructuredWidget = self.cachedWidgets[path]
            self.currentStructuredWidget.show()
            self.pathWidget.setPath(path)
        else:
            if "Type" not in path.get(self.scheme): #fimxe soon
                self.cachedWidgets[path] = StructuredWidget(unicode(path), path.get(self.data), path.get(self.scheme), self.openWidgetByPath, self)
                self.layout.addWidget(self.cachedWidgets[path])
                self.openWidgetByPath(path)
            else:
                pass


