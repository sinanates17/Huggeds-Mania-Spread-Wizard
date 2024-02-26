"""
This module contains class definitions for
SongWindow and related subwidgets.
"""

# pylint: disable=E0611,W0107,C0301,C0103
from os import listdir
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QListWidget, QListWidgetItem, QAbstractItemView, QScrollBar, QSlider, QVBoxLayout
from mutagen.wave import WAVE
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Statistician.parser import Parser
from Statistician.difficulty import Difficulty

class SongWindow(QWidget):
    """Defines a QWidget which will contain things specific to the selected mapset"""

    def __init__(self, parent):
        super().__init__(parent)

        self.diff_checkboxes = []
        self.widgets = []
        self.smoothing = 150 #+- time in ms to take a rolling average in the diff plots.
        self.sample_interval = 28 # Every x ms, sample the raw data to calculate a rolling average.
                                  #     Scales with smoothing to alleviate computational load.
        self.audio_path = ''
        self.length = 0

        self._init_ui()

    def _init_ui(self):
        """Help to condense __init__ a little."""
        self.setStyleSheet(
            """
            background-color: #2a2a2a;
            border-radius: 10px;
            """)

        self.label_title = QLabel(self)
        title_font = QFont("Nunito",32)
        self.label_title.setFont(title_font)
        self.label_title.setGeometry(30, 20, 1240, 60)
        self.label_title.setStyleSheet("""
            color: #dddddd;
            """)
        self.label_title.hide()
        self.widgets.append(self.label_title)

        self.label_creator = QLabel("Please select a beatmap folder...", self)
        creator_font = QFont("Nunito",24)
        self.label_creator.setFont(creator_font)
        self.label_creator.setGeometry(30, 80, 1240, 40)
        self.label_creator.setStyleSheet("""
            color: #888888;
            """)
        self.widgets.append(self.label_creator)

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
        self.diff_list.hide()
        self.widgets.append(self.diff_list)

        self.label_diff = QLabel("Select difficulties\nto compare", self)
        diff_font = QFont("Nunito",16)
        self.label_diff.setFont(diff_font)
        self.label_diff.setAlignment(Qt.AlignCenter)
        self.label_diff.setGeometry(30, 500, 180, 60)
        self.label_diff.setStyleSheet("""
            color: #888888
            """)
        self.label_diff.hide()
        self.widgets.append(self.label_diff)

        self.smoothing_slider = QSlider(Qt.Horizontal, self)
        self.smoothing_slider.setMinimum(50)
        self.smoothing_slider.setMaximum(811)
        self.smoothing_slider.setValue(150)
        self.smoothing_slider.valueChanged.connect(self.change_smoothing)
        self.smoothing_slider.setGeometry(270, 840, 800, 40)
        self.smoothing_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background: #666666;
                height: 40px;
                border-radius: 20px;
            }
            QSlider::handle:horizontal {
                background: #dddddd;
                height: 40px;
                width: 40px;
                border-radius: 20px;
            }
            """
        )
        self.smoothing_slider.hide()
        self.widgets.append(self.smoothing_slider)

        self.label_smoothing = QLabel(f"Smoothing: {self.smoothing}ms", self)
        self.label_smoothing.setFont(diff_font)
        self.label_smoothing.setGeometry(270, 800, 800, 40)
        self.label_smoothing.setAlignment(Qt.AlignCenter)
        self.label_smoothing.setStyleSheet("""
            color: #888888
            """)
        self.label_smoothing.hide()
        self.widgets.append(self.label_smoothing)

        self.plot = MapPlotWidget(self)
        self.plot.setGeometry(30,160,1240,310)
        self.plot.hide()
        self.widgets.append(self.plot)

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
        qp.end()

    def load_song(self, song_path):
        """Load in all the functional stuff when a song is selected."""

        for w in self.widgets:
            w.show()

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
        self.audio_path = ref.audio()

        audio = WAVE(self.audio_path)
        self.length = int(audio.info.length * 1000) #Extract the length in ms of the mapset's audio.

    def change_smoothing(self, v):
        """Connected to the smoothing slider."""

        self.smoothing = v if v <= 500 else (490 + 10*(v-500) if v <= 650 else 1950 + 50*(v-650))
        self.label_smoothing.setText(f"Smoothing: {self.smoothing}ms")
        self.sample_interval = self.smoothing ** (2/3)

        # Implement code to visually smooth the graph

    def calculate_density(self, smoothing, interval):
        """Calculate the series for 'Absolute Density' and 'Hand Balance'."""

class DiffItem(QListWidgetItem):
    """Defines a QCheckBox that also stores a Difficulty and graph series."""

    def __init__(self, parent, diff: Difficulty):
        super().__init__(parent)

        self._difficulty = diff
        self._name = diff.name()
        self.setText(diff.name())
        font = QFont("Nunito", 8)
        font.setBold(True)
        self.setFont(font)

        #Each series is a list of tuples of the format (Timestamp, Strain per second)
        #Strain per second could mean NPS or occurances per second of some pattern type.
        self.series = {
            "Absolute Density" : [],
            "Hand Balance" : [],
            #"LN Density" : [],
            #"LN Hand Balance" : [],
            #"RC Density" : [],
            #"RC Hand Balance" : [],
            #"Jack Intensity" : [],
            #"Jack Hand Balance" : [],
            #"Asynchronous Releases" : []
        }

    def difficulty(self) -> Difficulty:
        """Returns the object's Difficulty."""

        return self._difficulty

    def name(self) -> str:
        """Returns the contained Difficulty's name."""

        return self._name

class MapPlotWidget(QWidget):
    """Specialized widget with embedded MatPlotLib Plot for this application."""

    def __init__(self, parent=None):
        super(MapPlotWidget, self).__init__(parent)

        fig = Figure()
        #ax = fig.add_subplot(111)
        #ax.plot([1, 2, 3], [1, 2, 3])

        layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)
