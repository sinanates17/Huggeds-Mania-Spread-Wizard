"""Main script for Mapset Statistician."""

# pylint: disable=E0611, E0401
import sys
import requests
from PyQt5.QtWidgets import QApplication
from Interface.main_window import MainWindow

def get_latest() -> str:
    """Return the latest version of the application."""
    url = "http://github.com/sinanates17/Huggeds-Mania-Spread-Wizard/releases/latest"
    #pylint: disable=W3101
    r = requests.get(url, allow_redirects=True)
    latest_version = r.url.split('/')[-1]

    return latest_version

if __name__ == '__main__':
    VERSION = '1.0'
    LATEST = get_latest()
    app = QApplication(sys.argv)
    H = app.desktop().screenGeometry().height()
    w, h = int((H * .6) * 1.6), int(H * .6)
    window = MainWindow()
    window.check_update(VERSION, LATEST)
    window.setGeometry(100, 100, w, h)
    window.show()
    sys.exit(app.exec_())
