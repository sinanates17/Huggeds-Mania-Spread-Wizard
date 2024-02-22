"""This module contains a single class to define a song folder select list."""

# pylint: disable=E0611
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QSize, Qt

class SongList(QListWidget):
    """Define a QListWidget to act as a song folder selection menu."""

    def __init__(self, parent):
        super().__init__(parent)

        self.setWordWrap(True)
        self.setUniformItemSizes(True)
        self.setFocusPolicy(Qt.NoFocus)  # Remove focus rectangle
        self.setStyleSheet(#Style sheet taken from K0nomi with some changes
            """
            QListWidget {
                border-radius: 10px;
                border: 2px solid #111111;
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
                background-color: #333333;
            }
            
            QListWidget::item:selected:!active {
                background-color: #444444;
            }

            QListWidget::item:hover {
                background-color: #444444;
            }

            QScrollBar:vertical {
                border: none;
                background-color: #000000;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #444444;
                min-height: 20px;
                border-radius: 6px;
            }
            
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )

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
