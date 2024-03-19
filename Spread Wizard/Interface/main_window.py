"""This module contains a single class definition for Mapset Statistician's main window."""

# pylint: disable=E0611, E0401

from os import listdir, path
from json import dumps, load
from pyqt_frameless_window import FramelessMainWindow
from PyQt5.QtWidgets import QLabel
#from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Interface.title_bar import TitleBar #Import is being called from the root folder.
from Interface.song_folder_button import SongFolderButton
from Interface.song_list import SongList
from Interface.song_window import SongWindow

class MainWindow(FramelessMainWindow):
    """Define a specialized QMainWindow subclass for Mapset Statistician."""

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #111111")
        self.setTitleBarVisible(False)
        self.setPressToMove(False)
        self.setMinimumSize(400, 200)

        self.title = TitleBar(self)

        self.folder_path = None
        self.folder_button = SongFolderButton(self)

        self.song_list = SongList(self)
        self.song_list.max_increased.connect(self.refresh_songs)
        self.song_list.itemSelectionChanged.connect(
            lambda: self.song_window.load_song(
                f"{self.folder_path}/{self.song_list.currentItem().folder()}"))
        self.song_list.hide()

        self.song_window = SongWindow(self)
        self.song_window.hide()

        if "cache.json" not in listdir():
            with open("cache.json", "x", encoding="utf8") as f:
                data = {"folder_path": ""}
                folder_path = dumps(data)
                f.write(folder_path)

        with open("cache.json", "r", encoding="utf8") as f:
            data = load(f)
            if data["folder_path"] == "":
                pass
            else:
                self.folder_button.folder_path = data["folder_path"]
                self.refresh_songs()

        self.label_version = QLabel(self)
        font = QFont("Nunito", 10)
        font.setBold(True)
        self.label_version.setFont(font)
        self.label_version.setStyleSheet("color: #ab89b1;")

    def refresh_songs(self):
        """Update the song select menu."""

        self.song_window.show()
        self.song_list.show()

        self.folder_path = self.folder_button.folder_path
        with open("cache.json", "w", encoding="utf8") as f:
            data = {"folder_path": self.folder_path}
            folder_path = dumps(data)
            f.write(folder_path)

        if self.folder_path is None:
            pass
        else:
            dirs = listdir(self.folder_path)
            dirs.sort(key=lambda x: path.getmtime(self.folder_path + '/' + x)) # pylint: disable=W0108
            dirs.reverse()
            self.song_list.set_dir_list(dirs) #Useless currently
            subdirs = dirs[self.song_list.dir_count:self.song_list.max_songs - 1]
            for dir_ in subdirs:
                self.song_list.add_song(f"{self.folder_path}/{dir_}")
                #if len(self.song_list) >= self.song_list.max_songs:
                    #break
            self.folder_button.hide()

    # pylint: disable=C0103
    #These methods require camelcase cuz PyQt5 stinky poopoo
    def resizeEvent(self, event):
        """Handle resizing the application."""

        super().resizeEvent(event)

        w, h = event.size().width(), event.size().height()
        self.resize_children(w, h)

    def check_update(self, current: str, latest: str):
        """Show version info at the bottom of the screen."""
        if current == latest:
            self.label_version.setText(f"  Version {current}. You are up to date!")
        else:
            self.label_version.setText(f"  Version {current}. Download {latest} at http://github.com/sinanates17/Huggeds-Mania-Spread-Wizard/releases/latest")

    def setGeometry(self, ax: int, ay: int, aw: int, ah: int):
        """Modify setGeometry method to handle child widgets"""

        super().setGeometry(ax, ay, aw, ah)

        self.resize_children(aw, ah)

    def resize_children(self, w: int, h: int):
        """Handle resizing of child widgets."""

        self.title.setGeometry(0, 0, w, 30)

        bx, by = int(w / 2) - 120, int(h / 2) - 40
        self.folder_button.setGeometry(bx, by, 240, 80)

        ch = h - 90
        self.song_list.setGeometry(30, 60, 210, ch)

        dw = w - 300
        dh = h - 90
        self.song_window.setGeometry(270, 60, dw, dh)

        ey = h - 30
        self.label_version.setGeometry(0, ey, w, 30)
