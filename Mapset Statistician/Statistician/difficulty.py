"""This module contains a single class definition for a difficulty."""

from Statistician.note import Note
from Statistician.timing_point import TimingPoint
from Statistician.graph_data import RawGraphData

class Difficulty:
    """Represents a difficulty in a mapset."""

    def __init__(self):
        self._note_list = []
        self._timing_list = []
        self._name = ''
        self._keymode = -1
        self._artist = ''
        self._title = ''
        self._host = ''
        self._audio = ''

        self.data = { #Initially empty RawGraphData containers for the various stats to display
            "density"       : RawGraphData("Absolute Density")
            #"ln_density"   : RawGraphData("LN Density")      #Total LN-only density
            #"rc_density"   : RawGraphData("Rice Density")    #Total RC-only density
            #"jacks"        : RawGraphData("Jack Intensity")  #Stacks below threshold count as jacks
            #"asynch"       : RawGraphData("Asynch Releases") #Simple count of asynchronous releases
            #"hybridness"   : RawGraphData("Hybridness")      #RC intensity scaled by concurrent LNs
        }

    def __repr__(self) -> str:
        return f"[{self._name}]"

    def add_note(self, hit_object: Note):
        """Adds a Note object to self.note_list."""

        self._note_list.append(hit_object)

    def notes(self) -> list[Note]:
        """Returns the list of all notes."""

        return self._note_list

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
        self._note_list = [[] for i in range(lanes)]

    def keymode(self) -> int:
        """Return the keycount."""

        return self._keymode

    def set_artist(self, artist: str):
        """Sets the artist."""

        self._artist = artist

    def artist(self) -> str:
        """Returns the artist."""

        return self._artist

    def set_title(self, title: str):
        """Sets the title."""

        self._title = title

    def title(self) -> str:
        """Returns the title"""

        return self._title

    def set_host(self, host: str):
        """Sets the host."""

        self._host = host

    def host(self) -> str:
        """Returns the host."""

        return self._host

    def set_audio(self, audio: str):
        """Set the audio file"""

        self._audio = audio

    def audio(self) -> str:
        """Returns the audio file name."""

        return self._audio
