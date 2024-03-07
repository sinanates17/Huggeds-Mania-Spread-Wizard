"""
This module contains a class definition for SongWindow.
"""

# pylint: disable=E0611,W0107,C0301,C0103
from os import listdir
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QListWidget, QListWidgetItem, QAbstractItemView, QScrollBar, QSlider, QCheckBox
from audioread import audio_open
from Interface.map_plot_widget import MapPlotWidget
from Interface.diff_item import DiffItem
from Statistician.difficulty import Difficulty

class SongWindow(QWidget):
    """Defines a QWidget which will contain things specific to the selected mapset"""

    def __init__(self, parent):
        super().__init__(parent)

        self.diff_checkboxes = []
        self.widgets = []
        self.smoothing = 1500 #+- time in ms to take a rolling average in the diff plots.
        self.sample_interval = 600 # Every x ms, sample the raw data to calculate a rolling average.
                                  #     Scales with smoothing to alleviate computational load.
        self.threshold = 200 #Multi-use parameter depending on what graph is shown
        self.audio_path = ''
        self.length = 0

        #Create all child widgets then run _init_ui to set them up
        self.label_title = QLabel(self)
        self.label_creator = QLabel("Please select a beatmap folder...", self)
        self.diff_list = QListWidget(self)
        self.plot_list = QListWidget(self)
        self.label_diff = QLabel("Select difficulties\nto compare", self)
        self.label_plot = QLabel("Select what\nto compare", self)
        self.smoothing_slider = QSlider(Qt.Horizontal, self)
        self.threshold_slider = QSlider(Qt.Horizontal, self)
        self.threshold_mode = QCheckBox(self)
        self.label_smoothing = QLabel(f"Smoothing: {self.smoothing}ms", self)
        self.label_threshold = QLabel(f"Threshold: {self.threshold}ms", self)
        self.plot = MapPlotWidget(self)
        self._init_ui()

    def _init_ui(self):
        """Help to condense __init__ a little."""
        self.setStyleSheet(
            """
            background-color: #2a2a2a;
            border-radius: 10px;
            """)

        title_font = QFont("Nunito",32)
        self.label_title.setFont(title_font)
        self.label_title.setGeometry(30, 20, 1240, 60)
        self.label_title.setStyleSheet("""
            color: #dddddd;
            """)
        self.label_title.hide()
        self.widgets.append(self.label_title)

        creator_font = QFont("Nunito",24)
        self.label_creator.setFont(creator_font)
        self.label_creator.setGeometry(30, 80, 1240, 40)
        self.label_creator.setStyleSheet("""
            color: #888888;
            """)
        self.widgets.append(self.label_creator)

        scroll_bar1 = QScrollBar(self)
        scroll_bar1.setStyleSheet("""
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

        self.plot_list.setFocusPolicy(Qt.NoFocus)
        self.plot_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.plot_list.setVerticalScrollBar(scroll_bar1)
        self.plot_list.setLayoutDirection(Qt.RightToLeft)
        self.plot_list.setWordWrap(True)
        self.plot_list.setGeometry(1090, 575, 180, 305)
        self.plot_list.itemSelectionChanged.connect(
            self.process_key
        )

        self.plot_list.setStyleSheet("""
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
        self.plot_list.hide()
        self.widgets.append(self.plot_list)

        plot_font = QFont("Nunito", 8)
        plot_font.setBold(True)
        items = []
        for key in ["Absolute Density", "Hand Balance", "RC Density", "RC Balance", "LN Density",
                    "LN Balance", "RC/LN Balance", "Jack Intensity", "Jack Balance"]:
            item = QListWidgetItem(key)
            item.setFont(plot_font)
            self.plot_list.addItem(item)
            items.append(item)
        self.plot_list.setCurrentItem(items[0])

        scroll_bar2 = QScrollBar(self)
        scroll_bar2.setStyleSheet("""
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

        self.diff_list.setSelectionMode(QAbstractItemView.MultiSelection)
        self.diff_list.setFocusPolicy(Qt.NoFocus)
        self.diff_list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.diff_list.itemSelectionChanged.connect(
            self.process_key
        )
        self.diff_list.setWordWrap(True)
        self.diff_list.setGeometry(30, 575, 180, 305)
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
        self.diff_list.setVerticalScrollBar(scroll_bar2)
        self.diff_list.hide()
        self.widgets.append(self.diff_list)

        diff_font = QFont("Nunito",16)
        self.label_diff.setFont(diff_font)
        self.label_diff.setAlignment(Qt.AlignCenter)
        self.label_diff.setGeometry(30, 515, 180, 60)
        self.label_diff.setStyleSheet("""
            color: #888888
            """)
        self.label_diff.hide()
        self.widgets.append(self.label_diff)

        self.label_plot.setFont(diff_font)
        self.label_plot.setAlignment(Qt.AlignCenter)
        self.label_plot.setGeometry(1090, 515, 180, 60)
        self.label_plot.setStyleSheet("""
            color: #888888
            """)
        self.label_plot.hide()
        self.widgets.append(self.label_plot)

        self.smoothing_slider.setMinimum(3)
        self.smoothing_slider.setMaximum(100)
        self.smoothing_slider.setValue(15)
        self.smoothing_slider.valueChanged.connect(self.change_smoothing)
        self.smoothing_slider.setGeometry(240, 840, 820, 40)
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

        self.threshold_slider.setMinimum(2)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(20)
        self.threshold_slider.setStyleSheet(
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
        self.threshold_slider.setGeometry(240, 750, 820, 40)
        self.threshold_slider.valueChanged.connect(self.change_threshold)
        self.threshold_slider.hide()
        self.widgets.append(self.threshold_slider)

        self.label_threshold.setFont(diff_font)
        self.label_threshold.setGeometry(240, 710, 820, 40)
        self.label_threshold.setAlignment(Qt.AlignCenter)
        self.label_threshold.setStyleSheet("""
            color: #888888
            """)
        self.label_threshold.hide()
        self.widgets.append(self.label_threshold)

        self.threshold_mode.setFont(plot_font)
        self.threshold_mode.setText("Threshold mode")
        self.threshold_mode.setFont(diff_font)
        self.threshold_mode.setGeometry(240, 650, 180, 60)
        self.threshold_mode.stateChanged.connect(self.process_key)
        self.threshold_mode.setStyleSheet("""
            QCheckBox { background-color: none;
                        color: #888888 }
        """)
        self.threshold_mode.hide()
        self.widgets.append(self.threshold_mode)

        self.label_smoothing.setFont(diff_font)
        self.label_smoothing.setGeometry(240, 800, 820, 40)
        self.label_smoothing.setAlignment(Qt.AlignCenter)
        self.label_smoothing.setStyleSheet("""
            color: #888888
            """)
        self.label_smoothing.hide()
        self.widgets.append(self.label_smoothing)

        self.plot.setGeometry(-80,110,1460,420)#310)
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

        self.diff_list.clear()

        self.diff_checkboxes = []

        for f in listdir(song_path):
            if f.endswith(".osu"):
                with open(f"{song_path}/{f}", "r", encoding="utf8") as g:
                    for line in g.readlines():
                        if "Mode:" in line:
                            if "Mode: 3" in line:
                                diff = Difficulty.from_path(f"{song_path}/{f}")
                                box = DiffItem(self.diff_list, diff)
                                self.diff_checkboxes.append(box)
                                self.diff_list.addItem(box)
                            else:
                                break

        if len(self.diff_checkboxes) > 0:
            for w in self.widgets:
                w.show()

            ref = self.diff_checkboxes[0].difficulty()
            self.label_title.setText(f"{ref.artist()} - {ref.title()}")
            self.label_creator.setText(f"Beatmapset hosted by {ref.host()}")
            self.audio_path = f"{song_path}/{ref.audio()}"

            with audio_open(self.audio_path) as f:
                self.length = int(f.duration * 1000) #Extract the length in ms of the mapset's audio.

            self.process_key()

            self.plot.set_axisx(0, self.length)

    def change_smoothing(self, v):
        """Connected to the smoothing slider."""

        self.smoothing = v * 100
        self.label_smoothing.setText(f"Smoothing: {self.smoothing}ms")
        self.sample_interval = self.smoothing / 2.5 #self.smoothing ** (2/3)

        self.process_key()

    def change_threshold(self, v):
        """Connected to the threshold slider."""

        self.threshold = v * 10
        self.label_threshold.setText(f"Threshold: {self.threshold}ms")

        if self.threshold_mode.isChecked():
            self.process_key()

    def duration(self) -> int:
        """Returns the song length in ms"""

        return self.length

    def process_key(self):
        """Figure out which process method to call then update plot."""

        key = key = self.plot_list.currentItem().text()

        for diff in self.diff_checkboxes:
            match key:
                case "Absolute Density":
                    diff.process_density(self.smoothing, self.sample_interval, self.length)

                case "Hand Balance":
                    diff.process_density(self.smoothing, self.sample_interval, self.length)

                case "RC Density":
                    diff.process_rc_density(self.smoothing, self.sample_interval, self.length)

                case "RC Balance":
                    diff.process_rc_density(self.smoothing, self.sample_interval, self.length)

                case "LN Density":
                    diff.process_ln_density(self.smoothing, self.sample_interval, self.length)

                case "LN Balance":
                    diff.process_ln_density(self.smoothing, self.sample_interval, self.length)

                case "RC/LN Balance":
                    diff.process_rcln_balance(self.smoothing, self.sample_interval, self.length)

                case "Jack Intensity":
                    diff.process_jacks(self.smoothing, self.sample_interval, self.length,
                                       self.threshold, self.threshold_mode.isChecked())

                case "Jack Balance":
                    diff.process_jacks(self.smoothing, self.sample_interval, self.length,
                                       self.threshold, self.threshold_mode.isChecked())

        self.plot.update_plots(self.plot_list.currentItem().text(), self.diff_list.selectedItems())
