"""
This module contains class definitions for
SongWindow and related subwidgets.
"""

# pylint: disable=E0611,W0107
from os import listdir
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QCheckBox, QStyleOption, QStyle
from Statistician.parser import Parser
from Statistician.difficulty import Difficulty

class SongWindow(QWidget):
    """Defines a QWidget which will contain things specific to the selected mapset"""

    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet(
            """
            background-color: #2a2a2a;
            border-radius: 10px;
            """)

        self.diff_checkboxes = []

    def paintEvent(self, pe): #IDK How this works, but it needs to be here for style sheets to work.
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def load_song(self, song_path):
        """Load in all the functional stuff when a song is selected."""

        self.diff_checkboxes = []

        for f in listdir(song_path):
            if f.endswith(".osu"):
                diff = Parser.generate_difficulty(f"{song_path}/{f}")
                box = DiffCheckBox(self, diff)
                self.diff_checkboxes.append(box)

        #Style and place each checkbox on the SongWindow
        for i, box in enumerate(self.diff_checkboxes):
            box.setStyleSheet(
                            """
                            QCheckBox {
                                width: 120px;
                                height: 60px;
                                background-color: #333333;
                                border-radius: 10px
                            }
                            """)
            box.setGeometry(10, 10 + 120*i, 110, 60) #Left off here

class DiffCheckBox(QCheckBox):
    """Defines a QCheckBox that also stores a Difficulty."""

    def __init__(self, parent, diff: Difficulty):
        super().__init__(parent)

        self._difficulty = diff
        self._name = diff.name()
        self.setText(diff.name())

    def paintEvent(self, pe): 
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def difficulty(self) -> Difficulty:
        """Returns the object's Difficulty."""

        return self._difficulty
    
    def name(self) -> str:
        """Returns the contained Difficulty's name."""

        return self._name
