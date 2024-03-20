"""This module contains a single class definition for Mapset Statistician's main window."""

# pylint: disable=E0611, E0401

from os import listdir, path
from json import dumps, load
from copy import deepcopy
from pyqt_frameless_window import FramelessMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from Interface.title_bar import TitleBar #Import is being called from the root folder.
from Interface.song_folder_button import SongFolderButton
from Interface.song_list import SongList
from Interface.song_window import SongWindow
from Interface.search_bar import SearchBar

class MainWindow(FramelessMainWindow):
    """Define a specialized QMainWindow subclass for Mapset Statistician."""

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #111111")
        self.setTitleBarVisible(False)
        self.setPressToMove(False)
        self.setMinimumSize(400, 200)

        self.title = TitleBar(self)

        self.song_items = []

        self.folder_path = None
        self.folder_button = SongFolderButton(self)
        self.folder_button.folder_selected.connect(self.load_folder)

        self.search_bar = SearchBar(self)
        self.search_bar.hide()
        self.search_bar.search_made.connect(self.load_from_search)

        self.song_list = SongList(self)
        self.song_list.max_increased.connect(self.add_songs)
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
                self.folder_button.folder_path, self.folder_path = data["folder_path"], data["folder_path"]
                self.load_folder(self.folder_path)

        self.label_version = QLabel(self)
        font = QFont("Nunito", 10)
        font.setBold(True)
        self.label_version.setFont(font)
        self.label_version.setStyleSheet("color: #ab89b1;")

    def load_folder(self, folder):
        """Load the song select menu."""

        self.song_list.clear_songs()
        self.song_list.set_dir_list(listdir(folder))
        self.song_window.show()
        self.song_list.show()
        self.search_bar.show()

        self.folder_path = folder
        with open("cache.json", "w", encoding="utf8") as f:
            data = {"folder_path": self.folder_path}
            folder_path = dumps(data)
            f.write(folder_path)

        if self.folder_path is None:
            pass
        else:
            self.generate_song_items()
            self.add_songs()
            self.folder_button.hide()

    def add_songs(self):
        """Connected to song_list.max_increased"""

        if self.folder_path is None:
            pass
        elif self.search_bar.previous() == "":
            songs = self.song_items[self.song_list.count():self.song_list.max_songs - 1]
            for song in songs:
                self.song_list.addItem(deepcopy(song))

    def load_from_search(self, search_terms):
        """Use this when using the beatmap search feature"""

        self.song_list.clear_songs()

        if search_terms == []:
            self.add_songs()

        else:
            for song in self.song_items:
                for term in search_terms:
                    if term in song.metadata:
                        self.song_list.addItem(deepcopy(song))
                        continue

    def generate_song_items(self):
        """Create a SongListItem for every mapset"""

        if self.folder_path is None:
            pass
        else:
            self.song_items = []

            dirs = listdir(self.folder_path)
            dirs.sort(key=lambda x: path.getmtime(self.folder_path + '/' + x)) # pylint: disable=W0108
            dirs.reverse()
            for dir_ in dirs:
                song_item = SongList.generate_item(f"{self.folder_path}/{dir_}")
                self.song_items.append(song_item)

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

        ch = h - 140
        self.song_list.setGeometry(30, 110, 210, ch)

        dw = w - 300
        dh = h - 90
        self.song_window.setGeometry(270, 60, dw, dh)

        ey = h - 30
        self.label_version.setGeometry(0, ey, w, 30)

        self.search_bar.setGeometry(30, 60, 210, 40)
