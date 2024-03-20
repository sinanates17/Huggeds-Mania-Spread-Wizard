"""This module contains a single class to define a song folder select list."""

# pylint: disable=E0611
from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from Interface.expanding_scroll_bar import ExpandingScrollBar
from Interface.song_list_item import SongListItem

class SongList(QListWidget):
    """Define a QListWidget to act as a song folder selection menu."""

    max_increased = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.setWordWrap(True)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setUniformItemSizes(True)
        self.setFocusPolicy(Qt.NoFocus)  # Remove focus rectangle
        self.setStyleSheet(#Style sheet taken from K0nomi with some changes
            """
            QListWidget {
                border-radius: 10px;
                border: none;
                background-color: #111111;
                color: #ffffff;
            }
            
            QListWidget::item {
                background-color: #222222;
                padding: 15px;
                height: 60px;
                width: 160px;
                margin: 2px;
                border-radius: 5px;
            }
            
            QListWidget::item:selected {
                background-color: #666666;
            }
            
            QListWidget::item:selected:!active {
                background-color: #666666;
            }

            QListWidget::item:hover {
                background-color: #444444;
            }
            """
        )
        scroll_bar = ExpandingScrollBar(self)
        scroll_bar.max_reached.connect(self.increase_max_songs)
        scroll_bar.setStyleSheet("""
            QScrollBar {
                border: none;
                background-color: #111111;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle {
                background-color: #666666;
                min-height: 20px;
                border-radius: 5px;
            }
            
            QScrollBar::add-line{
                border: none;
                background: none;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            
            QScrollBar::sub-line {
                border: none;
                background: none;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            
            QScrollBar::add-page, QScrollBar::sub-page {
                background: none;
            }
            """)
        self.setVerticalScrollBar(scroll_bar)
        self.max_songs = 20
        self.dir_list = []
        self.dir_count = 0

    def clear_songs(self):
        """Clear all song folders."""

        self.clear()
        self.max_songs = 20
        #self.dir_list = []
        self.dir_count = 0

    @staticmethod
    def generate_item(folder_path: str) -> SongListItem:
        """Create a SongListItem from a beatmap folder."""

        font = QFont("Nunito", 10)
        font.setBold(True)
        item = SongListItem(folder_path)
        item.setFont(font)
        item.setForeground(QColor("#ab89b1"))
        item.setSizeHint(QSize(-1, 60))
        return item

    def increase_max_songs(self):
        """make room to load more songs."""
        a = len(self.dir_list)
        b = self.max_songs + 10
        self.max_songs = b if b < a else a

        self.max_increased.emit()

    def set_dir_list(self, dirs: list):
        """Set the list of directories."""
        self.dir_list = dirs
