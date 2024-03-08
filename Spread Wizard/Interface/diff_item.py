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
            "Absolute Density"      : { "timestamps" : [], "values" : []},
            "Hand Balance"          : { "timestamps" : [], "values" : []},
            "LN Density"            : { "timestamps" : [], "values" : []},
            "LN Balance"            : { "timestamps" : [], "values" : []},
            "RC Density"            : { "timestamps" : [], "values" : []},
            "RC Balance"            : { "timestamps" : [], "values" : []},
            "RC/LN Balance"         : { "timestamps" : [], "values" : []},
            "Jack Intensity"        : { "timestamps" : [], "values" : []},
            "Jack Hand Balance"     : { "timestamps" : [], "values" : []},
            "Asynchronous Releases" : { "timestamps" : [], "values" : []},
        }

    def empty_series(self):
        """Empties the series for use in changing smoothing."""

        self.series = {
            "Absolute Density"      : { "timestamps" : [], "values" : []},
            "Hand Balance"          : { "timestamps" : [], "values" : []},
            "LN Density"            : { "timestamps" : [], "values" : []},
            "LN Balance"            : { "timestamps" : [], "values" : []},
            "RC Density"            : { "timestamps" : [], "values" : []},
            "RC Balance"            : { "timestamps" : [], "values" : []},
            "RC/LN Balance"         : { "timestamps" : [], "values" : []},
            "Jack Intensity"        : { "timestamps" : [], "values" : []},
            "Jack Balance"          : { "timestamps" : [], "values" : []},
            "Asynchronous Releases" : { "timestamps" : [], "values" : []},
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

    def process_jacks(self, smoothing: int, interval: int, length: int, threshold: int, thresh_mode: bool):
        """Calculate the series for 'Jack Intensity' and 'Jack Balance'."""

        data = self._difficulty.data["jacks"]

        self.empty_series()
        j_times = self.series["Jack Intensity"]["timestamps"]
        j_values = self.series["Jack Intensity"]["values"]
        b_times = self.series["Jack Balance"]["timestamps"]
        b_values = self.series["Jack Balance"]["values"]

        t = 0
        self.max_ = length
        while t < self.max_:
            #Find indices only with strain points within the rolling average window.
            indices = [i for i, val in enumerate(data["timestamps"]) if val >= t - smoothing and val <= t + smoothing]

            if thresh_mode: #When thresh_mode is True, only jacks within threshold ms are counted as jacks, with strains of 1
                total = sum([1 for i in indices if data["strains"][i] <= threshold])
                r_total = sum([1 for i in indices if data["strains"][i] <= threshold and
                               data["hands"][i] == Hand.RIGHT or data["hands"][i] == Hand.AMBI])
                l_total = sum([1 for i in indices if data["strains"][i] <= threshold and
                               data["hands"][i] == Hand.LEFT or data["hands"][i] == Hand.AMBI])

                #strain per second = number of jacks within threshold per second
                sps = (total / (2 * smoothing + 1)) * 1000

                #This variable has the range [0,inf]
                ratio = 1 if l_total == 0 and r_total == 0 else (r_total / .001 if l_total == 0 else r_total / l_total)

                #Transform it into a new value in the range [-1,1]... f(x) = 1 - (2 / (x+1))
                balance = 1 - (2 / (ratio + 1))

            else: #When thresh_mode is False, determine jack strain using a sigmoid curve
                strain = []
                l_strain = []
                r_strain = []
                mid = 168 #no. of ms where a jack has a strain of 1. 168 = 1/2 snap at 180BPM

                for i in indices:
                    value = data["strains"][i]
                    strain.append(mid**2 / value**2) #1/4 minijack is 4x the strain as a 1/2 jack is 4x the strain as a 1/1 stack
                    if data["hands"][i] == Hand.RIGHT or data["hands"][i] == Hand.AMBI:
                        r_strain.append(mid**2 / value**2)

                    if data["hands"][i] == Hand.LEFT or data["hands"][i] == Hand.AMBI:
                        l_strain.append(mid**2 / value**2)

                total = sum(strain)
                r_total = sum(r_strain)
                l_total = sum(l_strain)
                sps = (total / (2 * smoothing + 1)) * 1000

                ratio = 1 if l_total == 0 and r_total == 0 else (r_total / .001 if l_total == 0 else r_total / l_total)

                #Transform it into a new value in the range [-1,1]... f(x) = 1 - (2 / (x+1))
                balance = 1 - (2 / (ratio + 1))


            j_times.append(t/1000)
            j_values.append(sps)
            b_times.append(t/1000)
            b_values.append(balance)

            t = t + interval

    def process_releases(self, smoothing: int, interval: int, length: int, threshold1: int, threshold2: int):
        "Calculate the series for 'Asynchronous Releases'."

        #threshold1 is the minimum LN length to be considered an LN
        #threshold2 is how many ms a release needs to be after an LN head or before an LN tail
            #To be considered asynchronous

        thresh1 = threshold1 if threshold1 > 0 else 2
        thresh2 = threshold2 if threshold2 > 0 else 2

        data = self._difficulty.data["asynch"]

        self.empty_series()
        times = self.series["Asynchronous Releases"]["timestamps"]
        values = self.series["Asynchronous Releases"]["values"]

        t = 0
        self.max_ = length
        while t < self.max_:
            #Find indices where the strain (release) release is within the rolling average window
            release_times = [val for i, val in enumerate(data["strains"]) if val >= t - smoothing and val <= t + smoothing and
                       val >= data["timestamps"][i] + thresh1]
                            #LNs shorter than threshold ms are not considered LNs

            total_strain = 0
            for release in release_times:
                subtotal_strain = sum([1 for k, val in enumerate(data["timestamps"]) if
                                       release >= val + thresh2 and
                                       release <= data["strains"][k] - thresh2 and
                                       data["strains"][k] - val >= thresh1])
                total_strain = total_strain + subtotal_strain

            sps = (total_strain / (2 * smoothing + 1)) * 1000

            times.append(t/1000)
            values.append(sps)

            t = t + interval
