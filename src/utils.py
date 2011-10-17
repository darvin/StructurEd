from PyQt4.QtGui import QPushButton, QToolBar, QToolButton, QTreeWidgetItemIterator
import os
import random
from unitreeserializer.format import Format

def get_or_create_dict_element(dictionary, key, default_value):
    if key in dictionary:
        return dictionary[key]
    else:
        dictionary[key] = default_value
        return dictionary[key]

def layout_set_sm_and_mrg(layout):
    layout.setSpacing(0)
    layout.setContentsMargins(0,0,0,0)

def get_home_dir():
    return os.getenv('USERPROFILE') or os.getenv('HOME')


class StyledButton(QPushButton):
    style = ""
    def __init__(self, *args, **kwargs):
        super(StyledButton, self).__init__(*args, **kwargs)
        self.setStyleSheet(self.style)

class PlusMinusWidget(QToolBar):
    def __init__(self, plus_callback, minus_callback, parent=None):
        super(PlusMinusWidget, self).__init__(parent)
        self._plus_button = QToolButton(self)
        self._minus_button = QToolButton(self)
        self._plus_button.setText("+")
        self._minus_button.setText("-")

        style = """
QToolButton {
    border: 1px solid #979797;
    border-radius: 0px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #F9F9F9, stop: 1 #E6E6E6);
    min-width: 20px;
    min-height: 20px;
    max-width: 20px;
    max-height: 20px;
}
QToolButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #dadbde, stop: 1 #f6f7fa);
    }
"""
        self._minus_button.setStyleSheet(style)
        self._plus_button.setStyleSheet(style)
        self._plus_button.clicked.connect(plus_callback)
        self._minus_button.clicked.connect(minus_callback)
        self.addWidget(self._plus_button)
        self.addWidget(self._minus_button)



def merge_dictionary(dst, src):
    stack = [(dst, src)]
    while stack:
        current_dst, current_src = stack.pop()
        for key in current_src:
            if key not in current_dst:
                current_dst[key] = current_src[key]
            else:
                if isinstance(current_src[key], dict) and isinstance(current_dst[key], dict) :
                    stack.append((current_dst[key], current_src[key]))
                else:
                    current_dst[key] = current_src[key]
    return dst


def random_str(st):
    return "{} {}".format(st, random.randint(1,100))



def get_format_filter(multi_options=False):
    formats = Format.get_formats()
    if multi_options:
        res = []
        for f in formats:
            res.append("{} ({})".format(f.description, " ".join(("*.{}".format(ext) for ext in f.extensions))))
        result = ";;".join(res)
        return result
    else:
        all_exts = ()
        for f in formats:
            all_exts += f.extensions
        return "Any data file ({})".format(" ".join(("*.{}".format(ext) for ext in all_exts)))


class TreeWidgetIter(QTreeWidgetItemIterator):
    def __init__(self, *args):
        QTreeWidgetItemIterator.__init__(self, *args)

    def __iter__(self):
        return self

    def next(self):
        self.__iadd__(1)
        value = self.value()
        if value:
            return self.value()
        else:
            raise StopIteration