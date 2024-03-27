"""This module contains a class definition for CheckButton"""

# pylint: disable=E0611,C0103
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal
#from PyQt5.QtCore import Qt

class CheckButton(QPushButton):
    """A QPushButton that acts like a check box"""

    state_changed = pyqtSignal()

    def __init__(self, parent, text=""):
        super().__init__(parent)

        self.setText(text)
        self.checked = True
        self.clicked.connect(self.toggle_checked)
        self.setStyleSheet("""
                QPushButton {
                    background-color: #888888;
                    color: #111111;
                    border-radius: 5px;
                    text-align: center;
                }

                QPushButton:hover {
                    background-color: #666666;
                }
            """)

    def toggle_checked(self):
        """Change checked state"""

        if self.checked:
            self.checked = False
            self.setStyleSheet("""
                QPushButton {
                    background-color: #444444;
                    color: #dddddd;
                    border-radius: 5px;
                    text-align: center;
                }

                QPushButton:hover {
                    background-color: #666666;
                }
            """)

        elif not self.checked:
            self.checked = True
            self.setStyleSheet("""
                QPushButton {
                    background-color: #888888;
                    color: #111111;
                    border-radius: 5px;
                    text-align: center;
                }

                QPushButton:hover {
                    background-color: #666666;
                }
            """)

        self.state_changed.emit()

    def isChecked(self) -> bool:
        """Override super()'s isChecked method"""
        return self.checked

    def setChecked(self, a0: bool):
        "Override setChecked"

        self.checked = a0
