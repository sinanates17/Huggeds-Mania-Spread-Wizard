"""Main script for Mapset Statistician."""

# pylint: disable=E0611
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
    window = MainWindow()
    window.disp_version(VERSION, LATEST)
    window.move(100,100)
    window.show()
    sys.exit(app.exec_())
