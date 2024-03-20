"""This module contains a single class to define a song folder select button"""

# pylint: disable=E0611
from tkinter.filedialog import askdirectory
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

class SongFolderButton(QPushButton):
    """Define a QPushButton to act as a song folder select button."""

    folder_selected = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent, text="🗀 Select Songs Folder")

        self.parent = parent

        font = QFont("Nunito", 12)
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet(
            """
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

        self.folder_path = ""
        self.clicked.connect(self.select_folder)

    def select_folder(self):
        """Open a file browser to select a song folder."""

        self.folder_path = askdirectory()
        self.folder_selected.emit(self.folder_path)
