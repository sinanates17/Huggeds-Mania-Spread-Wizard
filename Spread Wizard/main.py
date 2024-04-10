"""Main script for Mapset Statistician."""

# pylint: disable=E0611, E0401
import os
import sys
from shutil import rmtree
from subprocess import run
from requests import get
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from Interface.main_window import MainWindow
from Interface.no_ffmpeg_error import NoFFmpegError

def get_latest() -> str:
    """Return the latest version of the application."""
    url = "http://github.com/sinanates17/Huggeds-Mania-Spread-Wizard/releases/latest"
    #pylint: disable=W3101
    r = get(url, allow_redirects=True)
    latest_version = r.url.split('/')[-1]

    return latest_version

if __name__ == '__main__':

    os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'

    if "temp" in os.listdir():
        rmtree("temp")

    os.mkdir("temp")

    app = QApplication(sys.argv)

    ICON_PATH = os.path.join("Resources/icon.ico")#sys._MEIPASS, "Resources/icon.ico")
    SPLASH_PATH = os.path.join("Resources/splash.png")#sys._MEIPASS, "Resources/splash.png")

    splash = QSplashScreen(QPixmap(SPLASH_PATH))
    splash.show()

    try:
        check = run("where ffmpeg", shell=True, capture_output=True, text=True).stdout
        if check == "":
            raise NoFFmpegError

        VERSION = '1.2.0'
        LATEST = get_latest()
        HEIGHT = app.desktop().screenGeometry().height()
        W, H = int((HEIGHT * .6) * 1.6), int(HEIGHT * .6)
        W = 1200 if W < 1200 else W
        H = 790 if H < 790 else H

        window = MainWindow()
        window.set_icon(ICON_PATH)
        window.check_update(VERSION, LATEST)
        window.setGeometry(100, 100, W, H)
        window.show()

    except NoFFmpegError:
        warning = QMainWindow()
        warn_label = QLabel(warning, text="You need FFmpeg! Read the damn <a href=\"https://github.com/sinanates17/Huggeds-Mania-Spread-Wizard/tree/main?tab=readme-ov-file#how-to-install\">README</a>!")
        warn_label.setOpenExternalLinks(True)
        warning.setCentralWidget(warn_label)
        warning.show()

    app.setWindowIcon(QIcon(ICON_PATH))
    splash.close()

    sys.exit(app.exec_())
