"""This module contains a class definition for an expanding scroll bar."""

# pylint: disable=E0611, W0246, C0103
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtCore import pyqtSignal

class ExpandingScrollBar(QScrollBar):
    """A QScrollBar that emits a signal when the handle is at the max position."""

    max_reached = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

    def setValue(self, value):
        """Modify setValue method to emit the custom signal"""
        super().setValue(value)
        if value == self.maximum():
            self.max_reached.emit()
