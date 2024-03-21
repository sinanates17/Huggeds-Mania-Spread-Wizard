"""This module contains a single class definition for Mapset Statistician's main window."""

# pylint: disable=E0611, E0401

from os import listdir, path
from json import dumps, load
from copy import deepcopy
from pyqt_frameless_window import FramelessMainWindow
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
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

        font1 = QFont("Nunito", 10)
        font1.setBold(True)

        self.font2 = QFont("Nunito", 16)
        #font2.setBold(True)

        font3 = QFont("Nunito", 48)
        font3.setBold(True)

        self.title = TitleBar(self)

        self.song_items = []

        self.folder_path = ""
        self.folder_button = SongFolderButton(self)
        self.folder_button.folder_selected.connect(self.load_folder)

        self.search_bar = SearchBar(self)
        self.search_bar.hide()
        self.search_bar.search_made.connect(self.load_from_search)

        self.refresh_button = QPushButton(self, text="🗘")
        self.refresh_button.setFont(self.font2)
        self.refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #222222;
                color: #f9d5ff;
                border: none;
                border-radius: 10px; }
            QPushButton:hover {
                background-color: #444444;
                color: #f9d5ff;
                border: none; }
            """)
        self.refresh_button.clicked.connect(lambda: self.load_folder(self.folder_path))
        self.refresh_button.hide()

        self.song_list = SongList(self)
        self.song_list.max_increased.connect(self.add_songs)
        self.song_list.itemSelectionChanged.connect(
            lambda: self.song_window.load_song(
                f"{self.folder_path}/{self.song_list.currentItem().folder()}"))
        self.song_list.hide()

        self.song_window = SongWindow(self)
        self.song_window.hide()

        self.label_version = QLabel(self)
        self.label_version.setFont(font1)
        self.label_version.setStyleSheet("color: #ab89b1;")

        self.label_loading = QLabel(self, text="Processing folder, please wait...")
        self.label_loading.setFont(font3)
        self.label_loading.setAlignment(Qt.AlignCenter)
        self.label_loading.setStyleSheet("""
            background-color: rgba(0,0,0,0);
            color: #aaaaaa;
            border: none;
        """)
        #self.label_loading.hide()

        if "cache.json" not in listdir():
            with open("cache.json", "x", encoding="utf8") as f:
                data = {"folder_path": ""}
                folder_path = dumps(data)
                f.write(folder_path)

        with open("cache.json", "r", encoding="utf8") as f:
            data = load(f)
            #if data["folder_path"] == "":
            #    pass
            #else:
            self.folder_button.folder_path = data["folder_path"]
            self.folder_path = data["folder_path"]

        self.load_folder(self.folder_path)

    def load_folder(self, folder):
        """Load the song select menu."""

        if folder == "":
            return

        self.song_list.clear_songs()
        self.song_list.set_dir_list(listdir(folder))
        self.song_window.show()
        self.song_list.show()
        self.search_bar.show()
        self.refresh_button.show()
        print("show")
        self.label_loading.show()

        self.search_bar.clear_query()

        self.folder_path = folder
        self.resize_children(self.size().width(), self.size().height())
        self.folder_button.folder_path = folder
        with open("cache.json", "w", encoding="utf8") as f:
            data = {"folder_path": self.folder_path}
            folder_path = dumps(data)
            f.write(folder_path)

        if self.folder_path == "":
            pass
        else:
            self.generate_song_items()
            self.add_songs()

        print("hide")
        self.label_loading.hide()

    def add_songs(self):
        """Connected to song_list.max_increased"""

        if self.folder_path == "":
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

        if self.folder_path == "":
            pass
        else:
            self.song_items = []

            dirs = listdir(self.folder_path)
            dirs.sort(key=lambda x: path.getmtime(self.folder_path + '/' + x)) # pylint: disable=W0108
            dirs.reverse()
            for dir_ in dirs:
                full_path = f"{self.folder_path}/{dir_}"
                if path.isdir(full_path):
                    song_item = SongList.generate_item(full_path)
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
            self.label_version.setText(f"Version {current}. You are up to date!")
        else:
            self.label_version.setOpenExternalLinks(True)
            self.label_version.setText(f"Version {current} is outdated. Download the latest version, {latest}, <a href=\"http://github.com/sinanates17/Huggeds-Mania-Spread-Wizard/releases/latest\"> <font face=Nunito color=white> here</font></a>.")  #http://github.com/sinanates17/Huggeds-Mania-Spread-Wizard/releases/latest)

    def setGeometry(self, ax: int, ay: int, aw: int, ah: int):
        """Modify setGeometry method to handle child widgets"""

        super().setGeometry(ax, ay, aw, ah)

        self.resize_children(aw, ah)

    def resize_children(self, w: int, h: int):
        """Handle resizing of child widgets."""

        self.title.setGeometry(0, 0, w, 30)

        bx, by = int(w / 2) - 120, int(h / 2) - 40
        if self.folder_path == "":
            self.folder_button.setGeometry(bx, by, 240, 80)

        else:
            self.folder_button.setGeometry(140, 110, 100, 40)
            self.folder_button.setText("🗀")
            self.folder_button.setFont(self.font2)


        ch = h - 190
        self.song_list.setGeometry(30, 160, 210, ch)

        dw = w - 300
        dh = h - 90
        self.song_window.setGeometry(270, 60, dw, dh)

        ey = h - 30
        self.label_version.setGeometry(10, ey, w, 30)

        self.search_bar.setGeometry(30, 60, 210, 40)

        self.refresh_button.setGeometry(30, 110, 100, 40)

        fh = h - 30
        self.label_loading.setGeometry(0, 30, w, fh)
