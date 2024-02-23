"""
This module contains class definitions for
SongWindow and related subwidgets.
"""

# pylint: disable=E0611,W0107
from os import listdir
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
#from PyQt5.QtCore import
from PyQt5.QtWidgets import QWidget, QCheckBox, QStyleOption, QStyle, QLabel
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

        self.label_title = QLabel(self)
        title_font = QFont("Nunito",32)
        self.label_title.setFont(title_font)
        self.label_title.setGeometry(30, 20, 1240, 60)
        self.label_title.setStyleSheet("""
            color: #dddddd;
            """)

        self.label_creator = QLabel("Please select a beatmap folder...", self)
        creator_font = QFont("Nunito",24)
        self.label_creator.setFont(creator_font)
        self.label_creator.setGeometry(30, 80, 1240, 40)
        self.label_creator.setStyleSheet("""
            color: #888888;
            """)

    # pylint: disable=C0103,W0613
    def paintEvent(self, pe): #IDK How this works, but it needs to be here for style sheets to work.
        """Overwrite parent's paintEvent."""
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

        qp = QPainter()
        pen = QPen()
        qp.begin(self)
        pen.setWidth(3)
        pen.setColor(QColor(17, 17, 17))
        qp.setPen(pen)
        qp.drawLine(0, 130, 1300, 130)
        qp.drawLine(240, 130, 240, 1000)
        qp.end()

    def load_song(self, song_path):
        """Load in all the functional stuff when a song is selected."""

        for box in self.diff_checkboxes:
            box.deleteLater()
        self.diff_checkboxes = []

        for f in listdir(song_path):
            if f.endswith(".osu"):
                diff = Parser.generate_difficulty(f"{song_path}/{f}")
                box = DiffCheckBox(self, diff)
                self.diff_checkboxes.append(box)

        ref = self.diff_checkboxes[0].difficulty()
        self.label_title.setText(f"{ref.artist()} - {ref.title()}")
        self.label_creator.setText(f"Beatmapset hosted by {ref.host()}")

        #Style and place each checkbox on the SongWindow
        for i, box in enumerate(self.diff_checkboxes):
            box.setStyleSheet(
                            """
                            QCheckBox {
                                background-color: #444444;
                                border-radius: 5px;
                                color: #ab89b1;
                            }
                            QCheckBox:checked {
                                background-color: #666666;
                            }
                            QCheckBox::indicator {
                                width: 15px;
                                height: 15px;
                                background-color: #888888;
                                border-radius: 5px;
                            }
                            """)
            box.setGeometry(30, 160 + 50*i, 180, 40) #Left off here
            box.show()


class DiffCheckBox(QCheckBox):
    """Defines a QCheckBox that also stores a Difficulty."""

    def __init__(self, parent, diff: Difficulty):
        super().__init__(parent)

        self._difficulty = diff
        self._name = diff.name()
        self.setText(diff.name())
        font = QFont("Nunito", 8)
        font.setBold(True)
        self.setFont(font)

    def difficulty(self) -> Difficulty:
        """Returns the object's Difficulty."""

        return self._difficulty

    def name(self) -> str:
        """Returns the contained Difficulty's name."""

        return self._name
