"""
This module contains a class definition for SongWindow.
"""

# pylint: disable=E0611,W0107,C0301,C0103
import tempfile
from os import listdir
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QDesktopServices
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle, QLabel, QListWidget, QListWidgetItem, QAbstractItemView, QScrollBar, QPushButton
from pydub import AudioSegment
from Interface.map_plot_widget import MapPlotWidget
from Interface.diff_item import DiffItem
from Interface.slider_unclickable import SliderUnclickable
from Interface.check_button import CheckButton
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
        self.threshold2 = 200
        self.audio_path = ''
        self.length = 0

        #self.worker = ProcessingPool()

        #Create all child widgets then run _init_ui to set them up
        self.label_title = QLabel(self)

        self.label_creator = QLabel("Please select a beatmap folder...", self)

        self.diff_list = QListWidget(self)
        self.diff_list.itemSelectionChanged.connect(
            self.process_key
        )

        self.sel_all = QPushButton(self)
        self.sel_all.clicked.connect(self.diff_list.selectAll)

        self.desel_all = QPushButton(self)
        self.desel_all.clicked.connect(self.diff_list.clearSelection)

        self.plot_list = QListWidget(self)
        self.plot_list.itemSelectionChanged.connect(
            self.process_key
        )

        #self.label_diff = QLabel("Select difficulties\nto compare", self)

        #self.label_plot = QLabel("Select what\nto compare", self)

        self.smoothing_slider = SliderUnclickable(Qt.Horizontal, self)
        self.smoothing_slider.valueChanged.connect(self.change_smoothing)
        self.smoothing_slider.sliderReleased.connect(self.process_key)

        self.threshold_slider = SliderUnclickable(Qt.Horizontal, self)
        self.threshold_slider.valueChanged.connect(self.change_threshold)
        self.threshold_slider.sliderReleased.connect(self.process_key)

        self.threshold2_slider = SliderUnclickable(Qt.Horizontal, self)
        self.threshold2_slider.valueChanged.connect(self.change_threshold)
        self.threshold2_slider.sliderReleased.connect(self.process_key)

        self.threshold_mode = CheckButton(self, "Alt. Calculator")
        self.threshold_mode.state_changed.connect(self.process_key)

        self.label_smoothing = QLabel(f"Smoothing: {self.smoothing}ms", self)

        self.label_threshold = QLabel(f"Threshold 1: {self.threshold}ms", self)

        self.label_threshold2 = QLabel(f"Threshold 2: {self.threshold}ms", self)

        self.plot = MapPlotWidget(self)

        self.thresh1_desc = ""

        self.thresh2_desc = ""

        self.audio_player = QMediaPlayer(self)
        #self.audio_player.setNotifyInterval(20)
        #self.audio_player.positionChanged.connect(self.while_playing)

        self.audio_scrubber = SliderUnclickable(Qt.Horizontal, self)
        self.audio_scrubber.valueChanged.connect(self.seek)
        #self.audio_scrubber.valueChanged.connect(self.audio_player.setPosition)

        self.audio_volume = SliderUnclickable(Qt.Horizontal, self)
        self.audio_volume.valueChanged.connect(self.audio_player.setVolume)

        self.audio_button = CheckButton(self, "⏵")
        self.audio_button.state_changed.connect(self.toggle_playback)

        self.audio_mute = CheckButton(self, "🕪")
        self.audio_mute.state_changed.connect(self.toggle_mute)

        self.audio_timer = QTimer(self)
        self.audio_timer.timeout.connect(self.while_playing)

        self.audio_timestamp = QPushButton(self)
        self.audio_timestamp.pressed.connect(lambda: self.open_timestamp(self.audio_timestamp.text()))

        self.audio_media = QMediaContent()

        self._init_ui()

    def _init_ui(self):
        """Help to condense __init__ a little."""

        diff_font = QFont("Nunito", 12)#14)
        diff_font.setBold(True)

        self.setStyleSheet(
            """
            background-color: #2a2a2a;
            border-radius: 10px;
            """)

        title_font = QFont("Nunito",32)
        self.label_title.setFont(title_font)
        #self.label_title.setGeometry(30, 20, 1240, 60)
        self.label_title.setStyleSheet("""
            color: #dddddd;
            """)
        self.label_title.hide()
        self.widgets.append(self.label_title)

        creator_font = QFont("Nunito",24)
        self.label_creator.setFont(creator_font)
        #self.label_creator.setGeometry(30, 80, 1240, 40)
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
        #self.plot_list.setGeometry(1090, 575, 180, 305)

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
                height: 20px;
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
        # Following keys are in order of usefulness.
        for key in ["Absolute Density", "Jack Intensity", "Asynchronous Releases", "Hand Balance", "RC Density",
                    "RC Balance", "LN Density", "LN Balance", "RC/LN Balance", "Jack Balance"]:
            item = QListWidgetItem(key)
            item.setTextAlignment(Qt.AlignCenter)
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
        self.diff_list.setWordWrap(True)
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
                height: 20px;
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

        self.sel_all.setText("All")
        self.sel_all.setFont(diff_font)
        self.sel_all.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: #dddddd;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #666666;
            }
        """)
        self.sel_all.hide()
        self.widgets.append(self.sel_all)

        self.desel_all.setText("None")
        self.desel_all.setFont(diff_font)
        self.desel_all.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: #dddddd;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #666666;
            }
        """)
        self.desel_all.hide()
        self.widgets.append(self.desel_all)

        #self.label_diff.setFont(diff_font)
        #self.label_diff.setAlignment(Qt.AlignCenter)
        #self.label_diff.setStyleSheet("""
        #    color: #888888
        #    """)
        #self.label_diff.hide()
        #self.widgets.append(self.label_diff)

        #self.label_plot.setFont(diff_font)
        #self.label_plot.setAlignment(Qt.AlignCenter)
        #self.label_plot.setStyleSheet("""
        #    color: #888888
        #    """)
        #self.label_plot.hide()
        #self.widgets.append(self.label_plot)

        self.smoothing_slider.setMinimum(3)
        self.smoothing_slider.setMaximum(100)
        self.smoothing_slider.setValue(15)
        self.smoothing_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background: #666666;
                height: 14px;
                border-radius: 7px;
            }
            QSlider::handle:horizontal {
                background: #dddddd;
                height: 14px;
                width: 14px;
                border-radius: 7px;
            }
            """
        )
        self.smoothing_slider.hide()
        self.widgets.append(self.smoothing_slider)

        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(100)
        self.threshold_slider.setValue(20)
        self.threshold_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background: #666666;
                height: 14px;
                border-radius: 7px;
            }
            QSlider::handle:horizontal {
                background: #dddddd;
                height: 14px;
                width: 14px;
                border-radius: 7px;
            }
            """
        )
        self.threshold_slider.hide()
        self.widgets.append(self.threshold_slider)

        self.label_threshold.setFont(diff_font)
        self.label_threshold.setAlignment(Qt.AlignCenter)
        self.label_threshold.setStyleSheet("""
            color: #888888;
            background-color: transparent;
            """)
        self.label_threshold.hide()
        self.widgets.append(self.label_threshold)

        self.threshold2_slider.setMinimum(0)
        self.threshold2_slider.setMaximum(100)
        self.threshold2_slider.setValue(20)
        self.threshold2_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background: #666666;
                height: 14px;
                border-radius: 7px;
            }
            QSlider::handle:horizontal {
                background: #dddddd;
                height: 14px;
                width: 14px;
                border-radius: 7px;
            }
            """
        )
        self.threshold2_slider.hide()
        self.widgets.append(self.threshold2_slider)

        self.label_threshold2.setFont(diff_font)
        self.label_threshold2.setAlignment(Qt.AlignCenter)
        self.label_threshold2.setStyleSheet("""
            color: #888888;
            background-color: transparent;
            """)
        self.label_threshold2.hide()
        self.widgets.append(self.label_threshold2)

        self.threshold_mode.setFont(plot_font)
        self.threshold_mode.setFont(diff_font)
        self.threshold_mode.hide()
        self.widgets.append(self.threshold_mode)

        self.label_smoothing.setFont(diff_font)
        self.label_smoothing.setAlignment(Qt.AlignCenter)
        self.label_smoothing.setStyleSheet("""
            color: #888888;
            background-color: transparent;
            """)
        self.label_smoothing.hide()
        self.widgets.append(self.label_smoothing)

        self.plot.hide()
        self.widgets.append(self.plot)

        self.audio_scrubber.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background: #111111;
                height: 14px;
                border-radius: 7px;
            }
            QSlider::handle:horizontal {
                background: #dddddd;
                height: 14px;
                width: 14px;
                border-radius: 7px;
            }
            """
        )
        self.audio_scrubber.setMinimum(0)
        self.audio_scrubber.hide()
        self.widgets.append(self.audio_scrubber)

        self.audio_volume.setMinimum(0)
        self.audio_volume.setMaximum(100)
        self.audio_volume.setValue(50)
        self.audio_volume.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background: #666666;
                height: 14px;
                border-radius: 7px;
            }
            QSlider::handle:horizontal {
                background: #dddddd;
                height: 14px;
                width: 14px;
                border-radius: 7px;
            }
            """
        )
        self.audio_volume.hide()
        self.widgets.append(self.audio_volume)

        self.audio_timer.setInterval(33)
        #self.audio_timer.timeout.connect(self.update_scrubber)

        self.audio_button.setFont(creator_font)
        self.audio_button.hide()
        self.widgets.append(self.audio_button)

        self.audio_mute.setFont(creator_font)
        self.audio_mute.toggle_checked()
        self.audio_mute.hide()
        self.widgets.append(self.audio_mute)

        self.audio_timestamp.setFont(diff_font)
        self.audio_timestamp.setStyleSheet(
            """
            QPushButton {
                background-color: #444444;
                color: #dddddd;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #666666;
            }
            """
        )
        self.audio_timestamp.setText("00:00:000")
        self.audio_timestamp.hide()
        self.widgets.append(self.audio_timestamp)

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
        w = self.size().width()
        qp.drawLine(0, 130, w, 130)
        qp.end()

    def load_song(self, song_path):
        """Load in all the functional stuff when a song is selected."""

        self.diff_list.clear()
        self.audio_scrubber.setValue(0)
        self.audio_player.stop()

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

        self.diff_list.selectAll()

        if len(self.diff_checkboxes) > 0:
            for w in self.widgets:
                w.show()

            ref = self.diff_checkboxes[0].difficulty()
            self.label_title.setText(f"{ref.artist()} - {ref.title()}")
            self.label_creator.setText(f"Beatmapset hosted by {ref.host()}")
            self.audio_path = f"{song_path}/{ref.audio()}"

            if self.audio_path.endswith(".ogg"):
                self.audio_media = QMediaContent(QUrl.fromLocalFile(self.ogg_to_mp3(self.audio_path)))

            else:
                self.audio_media = QMediaContent(QUrl.fromLocalFile(self.audio_path))

            self.audio_player.setMedia(self.audio_media)
            self.length = AudioSegment.from_file(self.audio_path).duration_seconds * 1000 #Extract the length in ms of the mapset's audio.

            self.audio_scrubber.setMaximum(int(self.length))
            if self.audio_button.isChecked():
                self.audio_button.toggle_checked()

            self.process_key()

            self.plot.set_axisx(0, self.length / 1000)

    def ogg_to_mp3(self, ogg_file: str) -> str:
        """Generate a temporary mp3 file if the map's audio is ogg."""

        audio = AudioSegment.from_file(ogg_file, format="ogg")

        with tempfile.NamedTemporaryFile(suffix=".mp3", dir="temp", delete=False) as temp_mp3:
            temp_mp3.close()
            mp3_file = temp_mp3.name

            audio.export(mp3_file, format="mp3")

        return mp3_file

    def change_smoothing(self, v):
        """Connected to the smoothing slider."""

        self.smoothing = v * 100
        self.label_smoothing.setText(f"Smoothing: {self.smoothing}ms")
        self.sample_interval = self.smoothing / 2.5

    def change_threshold(self, v=None):
        """Connected to the threshold sliders."""

        self.threshold = self.threshold_slider.value() * 10
        self.label_threshold.setText(f"{self.thresh1_desc}: {self.threshold}ms")

        self.threshold2 = self.threshold2_slider.value() * 10
        self.label_threshold2.setText(f"{self.thresh2_desc}: {self.threshold2}ms")

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
                    self.threshold_slider.hide()
                    self.threshold2_slider.hide()
                    self.label_threshold.hide()
                    self.label_threshold2.hide()
                    self.threshold_mode.hide()

                case "Hand Balance":
                    diff.process_density(self.smoothing, self.sample_interval, self.length)
                    self.threshold_slider.hide()
                    self.threshold2_slider.hide()
                    self.label_threshold.hide()
                    self.label_threshold2.hide()
                    self.threshold_mode.hide()

                case "RC Density":
                    diff.process_rc_density(self.smoothing, self.sample_interval, self.length)
                    self.threshold_slider.hide()
                    self.threshold2_slider.hide()
                    self.label_threshold.hide()
                    self.label_threshold2.hide()
                    self.threshold_mode.hide()

                case "RC Balance":
                    diff.process_rc_density(self.smoothing, self.sample_interval, self.length)
                    self.threshold_slider.hide()
                    self.threshold2_slider.hide()
                    self.label_threshold.hide()
                    self.label_threshold2.hide()
                    self.threshold_mode.hide()

                case "LN Density":
                    diff.process_ln_density(self.smoothing, self.sample_interval, self.length)
                    self.threshold_slider.hide()
                    self.threshold2_slider.hide()
                    self.label_threshold.hide()
                    self.label_threshold2.hide()
                    self.threshold_mode.hide()

                case "LN Balance":
                    diff.process_ln_density(self.smoothing, self.sample_interval, self.length)
                    self.threshold_slider.hide()
                    self.threshold2_slider.hide()
                    self.label_threshold.hide()
                    self.label_threshold2.hide()
                    self.threshold_mode.hide()

                case "RC/LN Balance":
                    diff.process_rcln_balance(self.smoothing, self.sample_interval, self.length)
                    self.threshold_slider.hide()
                    self.threshold2_slider.hide()
                    self.label_threshold.hide()
                    self.label_threshold2.hide()
                    self.threshold_mode.hide()

                #pylint: disable=W0612
                case "Jack Intensity":
                    diff.process_jacks(self.smoothing, self.sample_interval, self.length,
                                       self.threshold, not self.threshold_mode.isChecked())
                    v = self.threshold_slider.hide() if self.threshold_mode.isChecked() else self.threshold_slider.show()
                    self.threshold2_slider.hide()
                    v = self.label_threshold.hide() if self.threshold_mode.isChecked() else self.label_threshold.show()
                    self.label_threshold2.hide()
                    self.threshold_mode.show()
                    self.thresh1_desc = "Max. Stack Distance"
                    self.change_threshold()

                case "Jack Balance":
                    diff.process_jacks(self.smoothing, self.sample_interval, self.length,
                                       self.threshold, not self.threshold_mode.isChecked())
                    v = self.threshold_slider.hide() if self.threshold_mode.isChecked() else self.threshold_slider.show()
                    self.threshold2_slider.hide()
                    v = self.label_threshold.hide() if self.threshold_mode.isChecked() else self.label_threshold.show()
                    self.label_threshold2.hide()
                    self.threshold_mode.show()
                    self.thresh1_desc = "Max. Stack Distance"
                    self.change_threshold()

                case "Asynchronous Releases":
                    diff.process_releases(self.smoothing, self.sample_interval, self.length,
                                       self.threshold, self.threshold2)
                    self.threshold_slider.show()
                    self.threshold2_slider.show()
                    self.label_threshold.show()
                    self.label_threshold2.show()
                    self.threshold_mode.hide()
                    self.thresh1_desc = "Min. LN Length"
                    self.thresh2_desc = "Overlap Tolerance"
                    self.change_threshold()

        self.plot.update_plots(self.plot_list.currentItem().text(), self.diff_list.selectedItems())

    def setGeometry(self, ax: int, ay: int, aw: int, ah: int):
        """Modify setGeometry method to handle resizing child widgets."""

        super().setGeometry(ax, ay, aw, ah)

        self.resize_children(aw, ah)

    def resize_children(self, w: int, h: int):
        """Handle resizing child widgets"""

        w = 900 if w < 900 else w
        h = 700 if h < 700 else h

        aw = w - 60
        self.label_title.setGeometry(30, 20, aw, 60)

        bw = aw
        self.label_creator.setGeometry(30, 80, bw, 40)

        cy = h - 210
        self.diff_list.setGeometry(30, cy, 180, 180)

        dx, dy = w - 210, cy
        self.plot_list.setGeometry(dx, dy, 180, 180)

        ey = dy - 50#60
        #self.label_diff.setGeometry(30, ey, 180, 60)

        fx, fy = dx, ey
        #self.label_plot.setGeometry(fx, fy, 180, 60)
        self.threshold_mode.setGeometry(fx, fy, 180, 40)

        gw = w - 480
        gy = h - 44
        self.smoothing_slider.setGeometry(240, gy, gw, 20)

        hw = gw
        hy = gy - 44
        self.threshold_slider.setGeometry(240, hy, hw, 20)

        iw = gw
        iy = hy - 44
        self.threshold2_slider.setGeometry(240, iy, iw, 20)

        jw = gw
        jy = gy - 32
        self.label_smoothing.setGeometry(240, jy, jw, 40)

        kw = gw
        ky = jy - 44
        self.label_threshold.setGeometry(240, ky, kw, 40)

        lw = gw
        ly = ky - 44
        self.label_threshold2.setGeometry(240, ly, lw, 40)

        mw, mh = w + 16, h - 370
        mx, my = -8, 124
        self.plot.setGeometry(mx, my, mw, mh)

        left = 60 / mw
        bottom = 60 / mh
        width = (mw - 90) / mw
        height = (mh - 90) / mh
        self.plot.ax.set_position([left, bottom, width, height])
        v = self.audio_scrubber.value()
        self.plot.trace_time(v / 1000)

        ny = ey
        self.sel_all.setGeometry(30, ny, 85, 40)
        self.desel_all.setGeometry(125, ny, 85, 40)

        ow = gw
        oy = ny
        self.audio_scrubber.setGeometry(240, oy, ow, 20)

        px, py = int(w / 2) - 145, oy + 30
        self.audio_button.setGeometry(px, py, 40, 40)

        qx, qy = px + 50, py + 10
        self.audio_volume.setGeometry(qx, qy, 80, 20)

        rx, ry = qx + 90, py
        self.audio_mute.setGeometry(rx, ry, 40, 40)

        sx, sy = rx + 50, ry
        self.audio_timestamp.setGeometry(sx, sy, 100, 40)

    def toggle_playback(self):
        """Handle toggling audio playback"""

        if self.audio_button.isChecked():
            self.audio_button.setText("⏸")
            self.audio_player.play()
            self.audio_timer.start()

        elif not self.audio_button.isChecked():
            self.audio_button.setText("⏵")
            self.audio_player.pause()
            self.audio_timer.stop()
            self.while_playing()

    def update_volume(self, v): #Currently unused
        """Handle adjustign playback volume"""

        self.audio_player.setVolume(v)

    def while_playing(self):
        """Do these while the audio player is playing"""

        v = self.audio_player.position()

        self.audio_scrubber.blockSignals(True)
        self.audio_scrubber.setValue(v)
        t = self.timestamp_form(v)
        self.audio_timestamp.setText(t)
        v = self.length if v > self.length else v
        self.plot.trace_time(v / 1000)
        self.audio_scrubber.blockSignals(False)

    def seek(self, v):
        """Connected to the audio scrubber"""

        self.audio_player.setPosition(v)
        #self.audio_player.stop()
        t = self.timestamp_form(v)
        self.audio_timestamp.setText(t)
        v = self.length if v > self.length else v
        self.plot.trace_time(v / 1000)

    def toggle_mute(self):
        """Connected to the mute button"""

        if self.audio_mute.isChecked():
            self.audio_mute.setText("🕨")
            self.audio_player.setMuted(True)

        elif not self.audio_mute.isChecked():
            self.audio_mute.setText("🕪")
            self.audio_player.setMuted(False)

    def open_timestamp(self, timestamp):
        """Open the timestamp in osu"""

        url = QUrl(f"osu://edit/{timestamp}")
        QDesktopServices.openUrl(url)

    def timestamp_form(self, t: int) -> str:
        """Convert a timestamp in ms to mm:ss:msms format"""

        ms = t % 1000
        s = int(t / 1000) % 60
        m = int(t / 60000)

        ms = "000" if ms == 0 else (f"00{ms}" if ms <= 9 else (f"0{ms}" if ms <= 99 else str(ms)))
        s = f"0{s}" if s <= 9 else str(s)
        m = f"0{m}" if m <= 9 else str(m)

        return f"{m}:{s}:{ms}"
