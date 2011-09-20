from structured.main_window import MainWindow
from PyQt4.QtGui import *
import os, sys


DEBUG = True
if __name__=="__main__":

    app = QApplication(sys.argv)

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