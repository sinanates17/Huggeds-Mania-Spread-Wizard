"""This module contains a class definition for a note, and an Enum representing either hand."""

from enum import Enum

class Hand(Enum):
    """Represents which hand a note is played by."""

    LEFT = -1
    AMBI = 0
    RIGHT = 1
    NONE = None

class Note:
    """Defines a single note."""

    def __init__(self, lane, start_time, note_type, end_time, hand):
        self._lane = lane
        self._start_time = start_time
        self._note_type = note_type
        self._end_time = end_time
        self._length = end_time - start_time
        self._hand = hand

    @classmethod
    def from_parser(cls, line, keymode):
        """Class method made specifically for the Parser object"""

        l = line.split(',')

        lane = int(int(l[0])/(512/keymode))
        time = int(l[2])
        typ = int(l[3])
        end = time if type == 1 else int(l[5].split(':')[0])
        hand = Hand.AMBI

        if lane < (keymode/2) + .5:
            hand = Hand.LEFT
        elif lane > (keymode/2) + .5:
            hand = Hand.RIGHT

        return cls(lane, time, typ, end, hand)

    def __repr__(self):
        return str(self.__dict__)

    def is_rice(self): # Check if the note is rice.
        """Returns True if note is rice."""
        return self._note_type != 128

    def hand(self) -> Hand:
        """Returns what hand the note is played by."""

        return self._hand

    def lane(self) -> int:
        """Returns the lane of the note."""

        return self._lane

    def time_start(self) -> int:
        """Returns the timestamp of the note."""

        return self._start_time

    def time_end(self) -> int:
        """Returns the timestamp of the end of the note (same as the start if rice)."""

        return self._end_time
