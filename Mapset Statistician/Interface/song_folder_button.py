"""This module contains a single class to define a song folder select button"""

# pylint: disable=E0611
from tkinter import filedialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont

class SongFolderButton(QPushButton):
    """Define a QPushButton to act as a song folder select button."""

    def __init__(self, parent):
        super().__init__(parent, text="🗀 Select Songs Folder")

        self.parent = parent

        font = QFont("Nunito", 12)
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet(
            """QPushButton {
                background-color: #111111;
                color: #f9d5ff;
                border: none;
                border-radius: 5px; }
            QPushButton:hover {
                background-color: #333333;
                color: #f9d5ff;
                border: none; }"
            """
            )

        self.folder_path = None
        self.clicked.connect(self.select_folder)

    def select_folder(self):
        """Open a file browser to select a song folder."""

        self.folder_path = filedialog.askdirectory()
        self.parent.refresh_songs()
