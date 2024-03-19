"""This module contains a class definition for SearchBar"""

# pylint: disable=E0611
#from os import listdir
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SearchBar(QWidget):
    """A search bar with a button to signal a search"""

    search_made = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.empty_label = QLabel(self, text=" Search by metadata...")
        self.search_text = QTextEdit(self)
        self.search_text.textChanged.connect(self.check_empty)
        self.search_button = QPushButton(self, text="🔍")
        self.search_button.pressed.connect(self.on_button_pressed)

        self._init_ui()

    def _init_ui(self):
        """Condense __init__"""

        font = QFont("Nunito", 8)
        font.setBold(True)

        self.setStyleSheet(
            """
            background: transparent;
            """
        )

        self.empty_label.setFont(font)
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet(
            """
            background-color: #2a2a2a;
            border-radius: 10px;
            border: none;
            color: #ab89b1;
            """
        )

        self.search_text.setFont(font)
        self.search_text.setStyleSheet(
            """
            color: white;
            border: none;
            background: transparent;
            """
        )

        self.search_button.setStyleSheet(
            """
            QPushButton {
                background-color: #111111;
                color: #f9d5ff;
                border: none;
                border-radius: 5px; }
            QPushButton:hover {
                background-color: #333333;
                color: #f9d5ff;
                border: none; }
            """
        )

    def check_empty(self):
        """Show the empty_label if the search bar is empty"""

        text = self.search_text.toPlainText()

        if text == "":
            self.empty_label.show()

        else:
            self.empty_label.hide()

    def on_button_pressed(self):
        """Emits a custom signal when the search button is pressed."""

        search_terms = self.search_text.toPlainText().split()
        self.search_made.emit(search_terms)

    def setGeometry(self, x: int, y: int, w: int, h: int):
        """Modify setGeometry method to handle child widgets."""

        super().setGeometry(x, y, w, h)

        aw = w - 50
        self.search_text.setGeometry(0, 0, aw, h)
        self.empty_label.setGeometry(0, 0, aw, h)

        bw = 40
        bx = w - 40
        self.search_button.setGeometry(bx, 0, bw, h)
