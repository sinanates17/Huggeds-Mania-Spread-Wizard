"""Contains class definition for DiffItem."""

# pylint: disable=E0611,W0107,C0301,C0103
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from Statistician.difficulty import Difficulty
from Statistician.note import Hand

class DiffItem(QListWidgetItem):
    """Defines a QCheckBox that also stores a Difficulty and graph series."""

    def __init__(self, parent: QListWidget, diff: Difficulty):
        super().__init__(parent)

        self._parent = parent
        self._difficulty = diff
        self._name = diff.name()
        self.setText(diff.name())
        font = QFont("Nunito", 8)
        font.setBold(True)
        self.setFont(font)
        self._difficulty.calculate_master()

        self.series = {
            "Absolute Density" : { "timestamps" : [], "values" : []},
            "Hand Balance" : { "timestamps" : [], "values" : []},
            #"LN Density" : { "timestamps" : [], "values" : []},
            #"LN Hand Balance" : { "timestamps" : [], "values" : []},
            #"RC Density" : { "timestamps" : [], "values" : []},
            #"RC Hand Balance" : { "timestamps" : [], "values" : []},
            #"Jack Intensity" : { "timestamps" : [], "values" : []},
            #"Jack Hand Balance" : { "timestamps" : [], "values" : []},
            #"Asynchronous Releases" : { "timestamps" : [], "values" : []},
        }

    def empty_series(self) -> dict:
        """Simply returns an empty series for use in changing smoothing."""

        self.series = {
            "Absolute Density" : { "timestamps" : [], "values" : []},
            "Hand Balance" : { "timestamps" : [], "values" : []},
            #"LN Density" : { "timestamps" : [], "values" : []},
            #"LN Hand Balance" : { "timestamps" : [], "values" : []},
            #"RC Density" : { "timestamps" : [], "values" : []},
            #"RC Hand Balance" : { "timestamps" : [], "values" : []},
            #"Jack Intensity" : { "timestamps" : [], "values" : []},
            #"Jack Hand Balance" : { "timestamps" : [], "values" : []},
            #"Asynchronous Releases" : { "timestamps" : [], "values" : []},
        }

    def difficulty(self) -> Difficulty:
        """Returns the object's Difficulty."""

        return self._difficulty

    def name(self) -> str:
        """Returns the contained Difficulty's name."""

        return self._name

    def process_density(self, smoothing: int, interval: int, length: int):
        """Calculate the series for 'Absolute Density' and 'Hand Balance'."""

        data = self._difficulty.data["density"]

        self.empty_series()
        ad_times = self.series["Absolute Density"]["timestamps"]
        ad_values = self.series["Absolute Density"]["values"]
        hb_times = self.series["Hand Balance"]["timestamps"]
        hb_values = self.series["Hand Balance"]["values"]

        t = 0
        max_ = length + 2 * smoothing
        while t < max_:
            #Find indices only with strain points within the rolling average window
            indices = [i for i, val in enumerate(data["timestamps"]) if val >= t - smoothing and val <= t + smoothing]
            total = sum([data["strains"][i] for i in indices])

            #Get the notes (strain) per second of this window
            nps = (total / (2 * smoothing + 1)) * 1000

            #Strain in the middle column counts for both hands
            l_total = sum([data["strains"][i] for i in indices if data["hands"][i] == Hand.LEFT or data["hands"][i] == Hand.AMBI])
            r_total = sum([data["strains"][i] for i in indices if data["hands"][i] == Hand.RIGHT or data["hands"][i] == Hand.AMBI])

            #This variable has the range [0,inf]
            ratio = -1 if l_total == 0 else r_total / l_total

            #Transform it into a new value in the range [-1,1]... f(x) = 1 - (2 / (x+1))
            balance = -1 if ratio == -1 else 1 - (2 / (ratio + 1))

            ad_times.append(t)
            ad_values.append(nps)
            hb_times.append(t)
            hb_values.append(balance)

            t = t + interval
