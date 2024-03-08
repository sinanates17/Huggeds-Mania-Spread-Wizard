"""This module contains a single class definition for a timing point"""

class TimingPoint:
    """
    Defines a timing point. All __init__ arguments should be passed as
    strings since they are meant to be taken directly from a .osu file.
    """

    def __init__(self, time, beat_length, meter, sample_set,
                 sample_index, volume, uninherited, effects):
        self._time = int(float(time))
        self._beat_length = float(beat_length)
        self._meter = int(meter)
        self._sample_set = int(sample_set)
        self._sample_index = int(sample_index)
        self._volume = int(volume)
        self._uninherited = False if uninherited == '0' else True #Convert inheritedness to bool
        self._effects = int(effects)

    @classmethod
    def from_dot_osu(cls, line):
        """Classmethod made specifically for the Parser."""

        l = line.split(',')

        return cls(l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7])

    def __repr__(self):
        return str(self.__dict__)

    def is_inherited(self):
        """Return True if timing point is inherited."""

        return not self._uninherited

    def time(self) -> int:
        """Return the timestamp of the timing point."""

        return self._time

    def beat_length(self) -> float:
        """Return the beat length (inverse BPM) in ms."""

        return self._beat_length

    def bpm(self) -> float:
        """Return the BPM of the timing point."""

        return 60000/self._beat_length

    def meter(self) -> int:
        """Return the meter (beats per bar)"""

        return self._meter
