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
        self.max_ = 0

        self.series = {
            "Absolute Density" : { "timestamps" : [], "values" : []},
            "Hand Balance"     : { "timestamps" : [], "values" : []},
            "LN Density"       : { "timestamps" : [], "values" : []},
            "LN Balance"       : { "timestamps" : [], "values" : []},
            "RC Density"       : { "timestamps" : [], "values" : []},
            "RC Balance"       : { "timestamps" : [], "values" : []},
            "RC/LN Balance"    : { "timestamps" : [], "values" : []},
            #"Jack Intensity" : { "timestamps" : [], "values" : []},
            #"Jack Hand Balance" : { "timestamps" : [], "values" : []},
            #"Asynchronous Releases" : { "timestamps" : [], "values" : []},
        }

    def empty_series(self) -> dict:
        """Simply returns an empty series for use in changing smoothing."""

        self.series = {
            "Absolute Density" : { "timestamps" : [], "values" : []},
            "Hand Balance"     : { "timestamps" : [], "values" : []},
            "LN Density"       : { "timestamps" : [], "values" : []},
            "LN Balance"       : { "timestamps" : [], "values" : []},
            "RC Density"       : { "timestamps" : [], "values" : []},
            "RC Balance"       : { "timestamps" : [], "values" : []},
            "RC/LN Balance"    : { "timestamps" : [], "values" : []},
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
        self.max_ = length
        while t < self.max_:
            #Find indices only with strain points within the rolling average window
            indices = [i for i, val in enumerate(data["timestamps"]) if val >= t - smoothing and val <= t + smoothing]
            total = sum([data["strains"][i] for i in indices])

            #Get the notes (strain) per second of this window
            nps = (total / (2 * smoothing + 1)) * 1000

            #Strain in the middle column counts for both hands
            l_total = sum([data["strains"][i] for i in indices if data["hands"][i] == Hand.LEFT or data["hands"][i] == Hand.AMBI])
            r_total = sum([data["strains"][i] for i in indices if data["hands"][i] == Hand.RIGHT or data["hands"][i] == Hand.AMBI])

            #This variable has the range [0,inf]
            ratio = 1 if l_total == 0 and r_total == 0 else (r_total / .001 if l_total == 0 else r_total / l_total)

            #Transform it into a new value in the range [-1,1]... f(x) = 1 - (2 / (x+1))
            balance = 1 - (2 / (ratio + 1))

            ad_times.append(t/1000)
            ad_values.append(nps)
            hb_times.append(t/1000)
            hb_values.append(balance)

            t = t + interval

    def process_rc_density(self, smoothing: int, interval: int, length: int):
        """Calculate the series for 'RC Density' and 'RC Balance'."""

        data = self._difficulty.data["rc_density"]

        self.empty_series()
        rc_ad_times = self.series["RC Density"]["timestamps"]
        rc_ad_values = self.series["RC Density"]["values"]
        rc_hb_times = self.series["RC Balance"]["timestamps"]
        rc_hb_values = self.series["RC Balance"]["values"]

        t = 0
        self.max_ = length
        while t < self.max_:
            #Find indices only with strain points within the rolling average window
            indices = [i for i, val in enumerate(data["timestamps"]) if val >= t - smoothing and val <= t + smoothing]
            total = sum([data["strains"][i] for i in indices])

            #Get the notes (strain) per second of this window
            nps = (total / (2 * smoothing + 1)) * 1000

            #Strain in the middle column counts for both hands
            l_total = sum([data["strains"][i] for i in indices if data["hands"][i] == Hand.LEFT or data["hands"][i] == Hand.AMBI])
            r_total = sum([data["strains"][i] for i in indices if data["hands"][i] == Hand.RIGHT or data["hands"][i] == Hand.AMBI])

            #This variable has the range [0,inf]
            ratio = 1 if l_total == 0 and r_total == 0 else (r_total / .001 if l_total == 0 else r_total / l_total)

            #Transform it into a new value in the range [-1,1]... f(x) = 1 - (2 / (x+1))
            balance = 1 - (2 / (ratio + 1))

            rc_ad_times.append(t/1000)
            rc_ad_values.append(nps)
            rc_hb_times.append(t/1000)
            rc_hb_values.append(balance)

            t = t + interval

    def process_ln_density(self, smoothing: int, interval: int, length: int):
        """Calculate the series for 'LN Density' and 'LN Balance'."""

        data = self._difficulty.data["ln_density"]

        self.empty_series()
        ln_ad_times = self.series["LN Density"]["timestamps"]
        ln_ad_values = self.series["LN Density"]["values"]
        ln_hb_times = self.series["LN Balance"]["timestamps"]
        ln_hb_values = self.series["LN Balance"]["values"]

        t = 0
        self.max_ = length
        while t < self.max_:
            #Find indices only with strain points within the rolling average window
            indices = [i for i, val in enumerate(data["timestamps"]) if val >= t - smoothing and val <= t + smoothing]
            total = sum([data["strains"][i] for i in indices])

            #Get the notes (strain) per second of this window
            nps = (total / (2 * smoothing + 1)) * 1000

            #Strain in the middle column counts for both hands
            l_total = sum([data["strains"][i] for i in indices if data["hands"][i] == Hand.LEFT or data["hands"][i] == Hand.AMBI])
            r_total = sum([data["strains"][i] for i in indices if data["hands"][i] == Hand.RIGHT or data["hands"][i] == Hand.AMBI])

            #This variable has the range [0,inf]
            ratio = 1 if l_total == 0 and r_total == 0 else (r_total / .001 if l_total == 0 else r_total / l_total)

            #Transform it into a new value in the range [-1,1]... f(x) = 1 - (2 / (x+1))
            balance = 1 - (2 / (ratio + 1))

            ln_ad_times.append(t/1000)
            ln_ad_values.append(nps)
            ln_hb_times.append(t/1000)
            ln_hb_values.append(balance)

            t = t + interval

    def process_rcln_balance(self, smoothing: int, interval: int, length: int):
        """Calculate the series for 'RC/LN Balance'."""

        rc_data = self._difficulty.data["rc_density"]
        ln_data = self._difficulty.data["ln_density"]

        self.empty_series()
        rclnb_times = self.series["RC/LN Balance"]["timestamps"]
        rclnb_values = self.series["RC/LN Balance"]["values"]

        t = 0
        self.max_ = length
        while t < self.max_:
            #Find indices only with strain points within the rolling average window
            rc_indices = [i for i, val in enumerate(rc_data["timestamps"]) if val >= t - smoothing and val <= t + smoothing]
            ln_indices = [i for i, val in enumerate(ln_data["timestamps"]) if val >= t - smoothing and val <= t + smoothing]

            rc_total = sum([rc_data["strains"][i] for i in rc_indices])
            ln_total = sum([ln_data["strains"][i] for i in ln_indices])

            #This variable has the range [0,inf]
            ratio = 1 if ln_total == 0 and rc_total == 0 else (rc_total / .001 if ln_total == 0 else rc_total / ln_total)

            #Transform it into a new value in the range [-1,1]... f(x) = 1 - (2 / (x+1))
            balance = 1 - (2 / (ratio + 1))

            rclnb_times.append(t/1000)
            rclnb_values.append(balance)

            t = t + interval
