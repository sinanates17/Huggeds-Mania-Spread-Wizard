"""
This module contains class definitions for
SongWindow and related subwidgets.
"""

# pylint: disable=E0611,W0107
from os import listdir
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QCheckBox
from Statistician.parser import Parser
from Statistician.difficulty import Difficulty

class SongWindow(QWidget):
    """Defines a QWidget which will contain things specific to the selected mapset"""

    def __init__(self, parent):
        super().__init__(parent)

        self.diff_checkboxes = []

    def load_song(self, song_path):
        """Load in all the functional stuff when a song is selected."""

        self.diff_checkboxes = []

        for f in listdir(song_path):
            if f.endswith(".osu"):
                diff = Parser.generate_difficulty(f"{song_path}/{f}")
                box = DiffCheckBox(self, diff)
                self.diff_checkboxes.append(box)

        #Style and place each checkbox on the SongWindow
        for box in self.diff_checkboxes:
            box.setStyleSheet(
                            """
                            QCheckBox {
                                width: 120px;
                                height: 60px;
                                background-color: #333333;
                                border-radius: 10px
                            }
                            """) #Left off here

class DiffCheckBox(QCheckBox):
    """Defines a QCheckBox that also stores a Difficulty."""

    def __init__(self, parent, diff: Difficulty):
        super().__init__(parent)

        self._difficulty = diff

    def difficulty(self) -> Difficulty:
        """Returns the object's Difficulty."""

        return self._difficulty
