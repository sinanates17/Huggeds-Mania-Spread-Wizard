"""Main script for Mapset Statistician."""

# pylint: disable=E0611
import sys
from PyQt5.QtWidgets import QApplication
from Interface.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.move(100,100)
    window.show()
    sys.exit(app.exec_())
