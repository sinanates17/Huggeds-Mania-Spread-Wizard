"""This module contains a single class definition for a difficulty."""

from Statistician.note import Note
from Statistician.timing_point import TimingPoint

class Difficulty:
    """Represents a difficulty in a mapset."""

    def __init__(self, notes: list[Note], times: list[TimingPoint], name: str,
                 keymode: int, artist: str, title: str, host: str, audio: str):
        self._note_list = notes
        self._timing_list = times
        self._name = name
        self._keymode = keymode
        self._artist = artist
        self._title = title
        self._host = host
        self._audio = audio

        self.data = {
            "density"       : {"timestamps" : [], "strains" : [], "hands" : []},
            "ln_density"    : {"timestamps" : [], "strains" : [], "hands" : []},
            "rc_density"    : {"timestamps" : [], "strains" : [], "hands" : []},
            "jacks"         : {"timestamps" : [], "strains" : [], "hands" : []}, #strains = ms since previous note in column
            "asynch"        : {"timestamps" : [], "strains" : [], "hands" : []}  #strains = ln end time
            #"hybridness"   :
        }

    @classmethod
    def from_path(cls, diff_path: str):
        """
        Initialize a Difficulty object from the .osu file of a difficulty.
        Takes the full path to a .osu difficulty as a string.
        """

        with open(diff_path, 'r', encoding='utf8') as f:
            #timing = False
            mapping = False
            lines = f.readlines()
            for line in lines:
                if 'Version' in line:
                    name = line[8:-1]

                elif 'CircleSize' in line:
                    keymode = int(line[11:-1])

                elif 'Title:' in line:
                    title = line[6:-1]

                elif 'Artist:' in line:
                    artist = line[7:-1]

                elif 'Creator:' in line:
                    host = line[8:-1]

                elif "AudioFilename:" in line:
                    audio = line[15:-1]

                elif "[TimingPoints]" in line:
                    break

            timings = []
            notes = []

            for line in lines:
                if "[TimingPoints]" in line:
                    #timing = True
                    mapping = False

                elif "[HitObjects]" in line:
                    #timing = False
                    mapping = True

                #Not using TimingPoints for now.
                #elif timing and "," in line:
                    #point = TimingPoint.from_dot_osu(line[0:-1])
                    #timings.append(point)

                elif mapping and "," in line:
                    note = Note.from_dot_osu(line[0:-1], keymode)
                    notes.append(note)

            return cls(notes, timings, name, keymode, artist, title, host, audio)

    def __repr__(self) -> str:
        return f"[{self._name}]"

    def add_note(self, hit_object: Note):
        """Adds a Note object to self.note_list."""

        self._note_list.append(hit_object)

    def notes(self) -> list[Note]:
        """Returns the list of all notes."""

        return self._note_list

    def calculate_master(self):
        """Calls all the calculate_x methods"""

        self.calculate_density()
        self.calculate_jacks()

    def calculate_density(self):
        """Populate the 'density', 'rc_density', and 'ln_density', items in self.data"""

        for note in self._note_list:
            timestamp = note.time_start()
            value = 1
            hand = note.hand()
            self.data["density"]["timestamps"].append(timestamp)
            self.data["density"]["strains"].append(value)
            self.data["density"]["hands"].append(hand)

            if note.is_rice():
                self.data["rc_density"]["timestamps"].append(timestamp)
                self.data["rc_density"]["strains"].append(value)
                self.data["rc_density"]["hands"].append(hand)

            elif not note.is_rice():
                self.data["ln_density"]["timestamps"].append(timestamp)
                self.data["ln_density"]["strains"].append(value)
                self.data["ln_density"]["hands"].append(hand)

    def calculate_jacks(self):
        """Populate the 'jacks' item in self.data"""

        last_note = [-10000 for i in range(self.keymode())]

        for note in self._note_list:
            timestamp = note.time_start()
            value = timestamp - last_note[note.lane()]
            hand = note.hand()

            last_note[note.lane()] = timestamp

            self.data["jacks"]["timestamps"].append(timestamp)
            self.data["jacks"]["strains"].append(value)
            self.data["jacks"]["hands"].append(hand)

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
