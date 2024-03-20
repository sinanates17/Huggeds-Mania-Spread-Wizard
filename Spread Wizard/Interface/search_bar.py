"""This module contains a class definition for SearchBar"""

# pylint: disable=E0611, C0103
#from os import listdir
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SearchBar(QWidget):
    """A search bar with a button to signal a search"""

    search_made = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)

        self.search_text = QTextEdit(self)
        self.search_button = QPushButton(self, text="⮨")
        self.search_button.pressed.connect(self.on_button_pressed)
        self.last_query = ""

        self._init_ui()

    def _init_ui(self):
        """Condense __init__"""

        font = QFont("Nunito", 8)
        font.setBold(True)

        font2 = QFont("Nunito", 16)

        self.setStyleSheet(
            """
            background: transparent;
            """
        )

        self.search_text.setPlaceholderText("Search by metadata...")
        self.search_text.setLineWrapMode(QTextEdit.NoWrap)
        self.search_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.search_text.setFont(font)
        self.search_text.setStyleSheet(
            """
            QTextEdit {
                color: white;
                border: none;
                background-color: #2a2a2a;
                border-radius: 10px;
                padding-top: 9px;
            }
            """
        )

        self.search_button.setFont(font2)
        self.search_button.setStyleSheet(
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
            """
        )

    def on_button_pressed(self):
        """Emits a custom signal when the search button is pressed."""

        self.last_query = self.search_text.toPlainText()
        search_terms = self.search_text.toPlainText().lower().split()
        self.search_made.emit(search_terms)

    def setGeometry(self, x: int, y: int, w: int, h: int):
        """Modify setGeometry method to handle child widgets."""

        super().setGeometry(x, y, w, h)

        aw = w - 50
        self.search_text.setGeometry(0, 0, aw, h)

        bw = 40
        bx = w - 40
        self.search_button.setGeometry(bx, 0, bw, h)

    def previous(self) -> str:
        """Return the text in the search bar"""

        return self.last_query

    def clear_query(self):
        """Clear the last query"""

        self.last_query = ""
        self.search_text.setText("")