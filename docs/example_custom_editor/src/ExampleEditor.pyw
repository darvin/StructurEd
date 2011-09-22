from structured.main_window import MainWindow
from PyQt4.QtGui import *
import os, sys


class CityMainWindow(MainWindow):
    def save_data(self):
        #you can do something funny there
        super(CityMainWindow, self).save_data()


if __name__=="__main__":

    app = QApplication(sys.argv)

    app.setOrganizationName("SergeyKlimov")
    app.setOrganizationDomain("darvin.github.com")
    app.setApplicationName("ExampleEditor")


    data_paths = (
            os.path.join(os.getcwd(), "..", "resources"),
            os.getcwd(),
        )
    for base_path in data_paths:
        scheme_filename = os.path.join(base_path, "sample_citybuilder_scheme.plist")
        if os.path.exists(scheme_filename):
            mainwindow = CityMainWindow(fixed_scheme_filename=scheme_filename)
            mainwindow.show()
            break

    sys.exit(app.exec_())