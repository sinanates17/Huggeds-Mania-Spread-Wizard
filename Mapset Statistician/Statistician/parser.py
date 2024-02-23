"""This module contains a single class for a beatmap parser."""

from Statistician.difficulty import Difficulty
from Statistician.note import Note
from Statistician.timing_point import TimingPoint
from Statistician.graph_data import StrainObject

class Parser:
    """
    Define a specialized parser to process beatmap information.
    """

    @staticmethod
    def generate_difficulty(diff_path: str) -> Difficulty:
        """
        Create and return a Difficulty object from the .osu file of a difficulty.
        Takes the full path to a .osu difficulty as a string.
        """

        # pylint: disable=C0301
        #I found it more intuitive to build a Difficulty this way rather than by fashioning a classmethod for it

        new_diff = Difficulty()

        with open(diff_path, 'r', encoding='utf8') as f:
            for line in f.readlines():
                if 'Version' in line:
                    new_diff.set_name(line[8:-1])

                elif 'CircleSize' in line:
                    new_diff.set_keymode(int(line[11:-1]))

                elif 'Title:' in line:
                    new_diff.set_title(line[6:-1])

                elif 'Artist:' in line:
                    new_diff.set_artist(line[7:-1])

                elif 'Creator:' in line:
                    new_diff.set_host(line[8:-1])

                if new_diff.name() != '' and new_diff.keymode() != -1:
                    break #When the keymode and diff name are set.

            # Loop through second time because keymode needs to be set to start generating notes.
            for line in f.readlines():
                if 'Tags' in line or 'Bookmarks' in line or 'Title' in line or 'Artist' in line or 'Source' in line:
                    continue #Avoid potential conflicts with the last two cases.

                elif line.count(',') == 6: #Hit object lines have 6 commas.
                    note = Note.from_parser(line[0:-1], new_diff.keymode())
                    new_diff.add_note(note)

                elif line.count(',') == 7: #Timing point lines have 7 commas.
                    point = TimingPoint.from_parser(line[0:-1])
                    new_diff.add_timing_point(point)

        return new_diff

    @staticmethod
    def generate_density_data(diff: Difficulty):
        """Append StrainObjects into the "density" RawGraphData of diff."""

        data = diff.data["density"]

        for note in diff.notes():
            point = StrainObject(1.0, note.time_start(), note.hand)
            data.add_point(point)
