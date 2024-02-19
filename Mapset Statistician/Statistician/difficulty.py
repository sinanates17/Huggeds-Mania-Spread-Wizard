"""This module contains a single class definition for a difficulty."""

from note import Note
from timing_point import TimingPoint

class Difficulty:
    """Represents a difficulty in a mapset."""

    def __init__(self):
        self._note_list = []
        self._timing_list = []
        self._name = ''
        self._keymode = -1

    def __repr__(self) -> str:
        return f"[{self.name}]"

    def add_note(self, hit_object: Note):
        """Adds a Note object to self.note_list."""

        self._note_list.append(hit_object)

    def notes(self) -> list[Note]:
        """Returns the list of all notes."""

        return self._note_list()

    def add_timing_point(self, time_point: TimingPoint):
        """Adds a Note object to self.note_list."""

        self._timing_list.append(time_point)

    def timing(self) -> list[TimingPoint]:
        """Returns the list of all timing points"""

        return self._timing_list

    def set_name(self, ver: str):
        """Set the name of the difficulty."""

        self._name = ver

    def name(self) -> str:
        """Return the difficulty name."""

        return self._name

    def set_keymode(self, lanes: int):
        """Set the keymode of the difficulty."""

        self._keymode = lanes
        self.note_list = [[] for i in lanes]

    def keymode(self) -> int:
        """Return the keycount."""

        return self._keymode