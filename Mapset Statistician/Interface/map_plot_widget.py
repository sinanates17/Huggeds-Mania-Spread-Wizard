"""Contains a class definition for MapPlotWidget"""

# pylint: disable=E0611,W0107,C0301,C0103
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_gtk3 import (
    #NavigationToolbar2GTK3 as NavigationToolbar)
#from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from Interface.diff_item import DiffItem

class MapPlotWidget(QWidget):
    """Specialized widget with embedded MatPlotLib Plot for this application."""

    def __init__(self, parent=None):
        super(MapPlotWidget, self).__init__(parent)

        self.parent = parent
        self.fig, self.ax = plt.subplots()
        #self.ax = self.fig.add_subplot(111)
        self.ax.set(xlim=(0,10),ylim=(0,10))

        layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

    def set_axisx(self, lim: int):
        """Set x axis from 0 to lim"""
        self.ax.set(xlim=(0,lim))
        self.fig.canvas.draw()

    def set_axisy(self, lim: int):
        """Set y axis from 0 to lim"""
        self.ax.set(ylim=(0,lim))
        self.fig.canvas.draw()

    def update_plots(self, key: str, diffs: list[DiffItem]):
        """
        key is one of the keys in the DiffItem.series dicts.
        *series should be DiffItem.series dicts. Plots all info contained.
        """

        self.ax.cla()
        for data in [diff.series for diff in diffs]:
            x = data[key]["timestamps"]
            y = data[key]["values"]
            self.ax.plot(x,y)
        self.fig.canvas.draw()
