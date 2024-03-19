"""Main script for Mapset Statistician."""

# pylint: disable=E0611, E0401
from sys import exit as sys_exit, argv
from requests import get
from PyQt5.QtWidgets import QApplication
from Interface.main_window import MainWindow

def get_latest() -> str:
    """Return the latest version of the application."""
    url = "http://github.com/sinanates17/Huggeds-Mania-Spread-Wizard/releases/latest"
    #pylint: disable=W3101
    r = get(url, allow_redirects=True)
    latest_version = r.url.split('/')[-1]

    return latest_version

if __name__ == '__main__':
    VERSION = '1.0'
    LATEST = get_latest()
    app = QApplication(argv)
    HEIGHT = app.desktop().screenGeometry().height()
    W, H = int((HEIGHT * .6) * 1.6), int(HEIGHT * .6)
    W = 1000 if W < 1000 else W
    H = 790 if H < 790 else H
    window = MainWindow()
    window.check_update(VERSION, LATEST)
    window.setGeometry(100, 100, W, H)
    window.show()
    sys_exit(app.exec_())
