from PyQt4.QtGui import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton
from models import Path
from widgets import StructuredWidget


class LabelPath(QPushButton):
    def __init__(self, open_func, parent=None):
        super(LabelPath, self).__init__(parent)
        self.path = None
        self.open_func = open_func
        self.clicked.connect(self.openPath)

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
        self.layout = QHBoxLayout(self)
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
#            try:
            self.cachedWidgets[path] = StructuredWidget(unicode(path), path.get(self.data), path.get(self.scheme), self.openWidgetByPath, self)
#            except:
#                return
            self.layout.addWidget(self.cachedWidgets[path])
            self.openWidgetByPath(path)

