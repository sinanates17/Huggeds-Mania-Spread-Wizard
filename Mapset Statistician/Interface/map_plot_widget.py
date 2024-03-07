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
        self.ax.set_facecolor("black")
        self.fig.set_facecolor("#2a2a2a")
        self.fig.patch.set_alpha(0)

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['bottom'].set_color('white')

        layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.canvas)

    def set_axisx(self, lim0: int, lim1: int):
        """Set x axis from 0 to lim"""
        self.ax.set(xlim=(lim0,lim1))
        #self.fig.canvas.draw()

    def set_axisy(self, lim0: int, lim1: int):
        """Set y axis from 0 to lim"""
        self.ax.set(ylim=(lim0,lim1))
        #self.fig.canvas.draw()

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

        self.ax.set_title(key, color='white')

        match key:
            case "Absolute Density":
                self.ax.set_ylabel("NPS")

            case "Hand Balance":
                self.set_axisy(-1.1,1.1)
                self.ax.set_ylabel("Hand Bias")

            case "RC Density":
                self.ax.set_ylabel("NPS")

            case "RC Balance":
                self.set_axisy(-1.1,1.1)
                self.ax.set_ylabel("Hand Bias")

            case "LN Density":
                self.ax.set_ylabel("NPS")

            case "LN Balance":
                self.set_axisy(-1.1,1.1)
                self.ax.set_ylabel("Hand Bias")

            case "RC/LN Balance":
                self.set_axisy(-1.1,1.1)
                self.ax.set_ylabel("RC/LN Bias")

            case "Jack Intensity":
                self.ax.set_ylabel("Strain")

            case "Jack Balance":
                self.set_axisy(-1.1,1.1)
                self.ax.set_ylabel("Hand Bias")

            case "Asynchronous Releases":
                self.ax.set_ylabel("Strain")

        if len(diffs) > 0:
            self.set_axisx(0, diffs[0].max_ / 1000) #Set x axes strinctly from 0 to the map length in s.
        self.ax.set_xlabel("Time")
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.minorticks_on()
        self.ax.grid(visible=True, which='major', axis='both', color='#444444')
        self.ax.grid(visible=True, which='minor', axis='both', color='#222222')
        self.fig.canvas.draw()
