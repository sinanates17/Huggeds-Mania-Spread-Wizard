"""This module contains a single class to define a song folder select list."""

# pylint: disable=E0611
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QScrollBar
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QSize, Qt

class SongList(QListWidget):
    """Define a QListWidget to act as a song folder selection menu."""

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
        scroll_bar = QScrollBar(self)
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

    def clear_songs(self):
        """Clear all song folders."""

        self.clear()

    def add_song(self, folder_name: str):
        """Add a song folder."""

        font = QFont("Nunito", 10)
        font.setBold(True)
        item = QListWidgetItem()
        item.setText(folder_name)
        item.setFont(font)
        item.setForeground(QColor("#ab89b1"))
        item.setSizeHint(QSize(-1, 60))
        self.addItem(item)
