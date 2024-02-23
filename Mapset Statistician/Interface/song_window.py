"""
This module contains class definitions for
SongWindow and related subwidgets.
"""

# pylint: disable=E0611,W0107,C0301
from os import listdir
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QListWidget, QListWidgetItem, QAbstractItemView, QScrollBar, QSlider
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
        self.smoothing = 150

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

        self.diff_list = QListWidget(self)
        self.diff_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.diff_list.setFocusPolicy(Qt.NoFocus)
        self.diff_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.diff_list.setWordWrap(True)
        self.diff_list.setGeometry(30, 560, 180, 320)
        self.diff_list.setStyleSheet("""
            QListWidget {
                border-radius: 10px;
                border: none;
                background-color: #2a2a2a;
                color: #dddddd;
            }
            
            QListWidget::item {
                background-color: #444444;
                padding: 5px;
                height: 40px;
                width: 148px;
                margin: 2px;
                border-radius: 5px;
            }
            
            QListWidget::item:selected {
                background-color: #888888;
                border: none;
            }

            QListWidget::item:hover {
                background-color: #666666;
            }

            QScrollBar {
                border: none;
                background-color: #2a2a2a;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle {
                background-color: #444444;
                min-height: 20px;
                border-radius: 6px;
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
        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet("""
            QScrollBar {
                border: none;
                background-color: #2a2a2a;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            
            QScrollBar::handle {
                background-color: #dddddd;
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
        self.diff_list.setVerticalScrollBar(scroll_bar)

        self.label_diff = QLabel("Select difficulties\nto compare", self)
        diff_font = QFont("Nunito",16)
        self.label_diff.setFont(diff_font)
        self.label_diff.setAlignment(Qt.AlignCenter)
        self.label_diff.setGeometry(30, 500, 180, 60)
        self.label_diff.setStyleSheet("""
            color: #888888
            """)

        self.smoothing_slider = QSlider(self)
        self.smoothing_slider.setMinimum(10)
        self.smoothing_slider.setMaximum(810)
        self.smoothing_slider.setValue(150)
        self.smoothing_slider.hide()
        # Implement a label showing the smoothing value.

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
        qp.drawLine(240, 500, 240, 1000)
        qp.end()

    def load_song(self, song_path):
        """Load in all the functional stuff when a song is selected."""

        self.diff_list.clear()

        self.diff_checkboxes = []

        for f in listdir(song_path):
            if f.endswith(".osu"):
                diff = Parser.generate_difficulty(f"{song_path}/{f}")
                box = DiffItem(self.diff_list, diff)
                self.diff_checkboxes.append(box)
                self.diff_list.addItem(box)

        ref = self.diff_checkboxes[0].difficulty()
        self.label_title.setText(f"{ref.artist()} - {ref.title()}")
        self.label_creator.setText(f"Beatmapset hosted by {ref.host()}")

    def change_smoothing(self, v):
        """Connected to the smoothing slider."""

        self.smoothing = v if v <= 500 else (500 + 10*(v-500) if v <= 650 else 2000 + 50*(v-650))

        # Implement code to visually smooth the graph

class DiffItem(QListWidgetItem):
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
