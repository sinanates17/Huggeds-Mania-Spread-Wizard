"""This module contains a single class definition for SongWindow"""

# pylint: disable=E0611,W0107
from PyQt5.QtWidgets import QWidget, QListWidgetItem

class SongWindow(QWidget):
    """Defines a QWidget which will contain things specific to the selected mapset"""

    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet('background-color: #2a2a2a;'
                           'border-radius: 10px;')

    # pylint: disable=C0103
    def setGeometry(self, ax: int, ay: int, aw: int, ah: int):
        """Set self's geometry and adjust all sub-widgets."""

        pass

    def load_song(self, item: QListWidgetItem):
        """Load in all the functional stuff when a song is selected."""

        print(item.text() if item is not None else 'None')
