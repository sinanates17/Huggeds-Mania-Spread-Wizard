"""This module contains a single class definition for Mapset Statistician's main window."""

# pylint: disable=E0611

from os import listdir, path
import json
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from Interface.title_bar import TitleBar #Import is being called from the root folder.
from Interface.song_folder_button import SongFolderButton
from Interface.song_list import SongList
from Interface.song_window import SongWindow

class MainWindow(QMainWindow):
    """Define a specialized QMainWindow subclass for Mapset Statistician."""

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #111111")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 1600, 1000)

        self.title = TitleBar(self)

        self.folder_path = None
        self.folder_button = SongFolderButton(self)
        x = int(self.size().width()/2)
        y = int(self.size().height()/2)
        self.folder_button.setGeometry(x-120, y-40, 240, 80)

        self.song_list = SongList(self)
        self.song_list.setGeometry(30, 60, 210, 910)
        self.song_list.itemSelectionChanged.connect(
            lambda: self.song_window.load_song(
                f"{self.folder_path}/{self.song_list.currentItem().text()}"))
        self.song_list.hide()

        self.song_window = SongWindow(self)
        self.song_window.setGeometry(270, 60, 1300, 910)
        self.song_window.hide()

        if "cache.json" not in listdir():
            with open("cache.json", "x", encoding="utf8") as f:
                data = {"folder_path": ""}
                folder_path = json.dumps(data)
                f.write(folder_path)

        with open("cache.json", "r", encoding="utf8") as f:
            data = json.load(f)
            if data["folder_path"] == "":
                pass
            else:
                self.folder_button.folder_path = data["folder_path"]
                self.refresh_songs()


    def refresh_songs(self):
        """Update the song select menu."""

        self.song_window.show()
        self.song_list.show()

        self.folder_path = self.folder_button.folder_path
        with open("cache.json", "w", encoding="utf8") as f:
            data = {"folder_path": self.folder_path}
            folder_path = json.dumps(data)
            f.write(folder_path)

        if self.folder_path is None:
            pass
        else:
            dirs = listdir(self.folder_path)
            dirs.sort(key=lambda x: path.getmtime(self.folder_path + '/' + x)) # pylint: disable=W0108
            dirs.reverse()
            for dir_ in dirs:
                self.song_list.add_song(dir_)
                if len(self.song_list) > 40:
                    break

    # pylint: disable=C0103
    #(These methods require camelcase cuz PyQt5)
    def resizeEvent(self, event):
        """Handle resizing the application."""

        super().resizeEvent(event)

        size = event.size()
        self.title.setGeometry(0, 0, size.width(), 30)
        self.song_list.setGeometry(30, 60, 210, size.height() - 90)
        #self.song_window.setGeometry(270, 60, size.height() - 90, size.width() - 300)
