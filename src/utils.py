from PyQt4.QtGui import QPushButton

def get_or_create_dict_element(dictionary, key, default_value):
    if key in dictionary:
        return dictionary[key]
    else:
        dictionary[key] = default_value
        return dictionary[key]

def layout_set_sm_and_mrg(layout):
    layout.setSpacing(0)
    layout.setContentsMargins(0,0,0,0)



class StyledButton(QPushButton):
    style = ""
    def __init__(self, *args, **kwargs):
        super(StyledButton, self).__init__(*args, **kwargs)
        self.setStyleSheet(self.style)