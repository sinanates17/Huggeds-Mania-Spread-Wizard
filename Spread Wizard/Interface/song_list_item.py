"""This module contains a class definition for SongListItem"""

# pylint: disable=E0611
from os import listdir
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor

FONT = QFont("Nunito", 10)
FONT.setBold(True)

class SongListItem(QListWidgetItem):
    """
    Defines a SongListItem that additionally stores 
    metadata about the song folder it represents.
    """

    def __init__(self, path: str):
        super().__init__()

        self.setTextAlignment(Qt.AlignCenter)

        self.metadata = "" #Combined metadata
        self.folder_path = path
        self.folder_name = path.split("/")[-1]
        self.artist = ""
        self.artist_unicode = ""
        self.title = ""
        self.title_unicode = ""
        self.mapper = ""
        self.source = ""
        self.tags = ""

        self.setFont(FONT)
        self.setForeground(QColor("#ab89b1"))
        self.setSizeHint(QSize(-1, 60))

        for file in listdir(self.folder_path):
            if file.endswith(".osu"):
                with open(f"{self.folder_path}/{file}", "r", encoding="utf8") as f:
                    for line in f.readlines():

                        if 'Title:' in line:
                            self.title = line[6:-1]

                        elif 'TitleUnicode:' in line:
                            self.title_unicode = line[13:-1]

                        elif 'Artist:' in line:
                            self.artist = line[7:-1]

                        elif 'ArtistUnicode:' in line:
                            self.artist_unicode = line[14:-1]

                        elif 'Creator:' in line:
                            self.mapper = line[8:-1]

                        elif 'Source:' in line:
                            self.source = line[7:-1] if len(line) > 7 else ""

                        elif 'Tags:' in line:
                            self.tags = line[5:-1] if len(line) > 5 else ""
                            break

                break #Get metadata only from the first .osu found in the folder.
                      #Metadata should match for all diffs on maps for ranked anyway.

        props = [self.artist, self. artist_unicode, self.title, self.title_unicode,
                 self.mapper, self.source, self.tags]

        for prop in props:
            for word in prop.split(" "):
                self.metadata = self.metadata + f"{word} "

        self.metadata = self.metadata.lower()
        self.setText(f"{self.artist} - {self.title}\n{self.mapper}")

    def folder(self) -> str:
        """Return the name of the song's folder"""
        return self.folder_name

    def path(self) -> str:
        """Return the path to the folder"""
        return self.folder_path

    def __deepcopy__(self, o):
        """Tell deepcopy how to copy an instance of this thing."""

        return SongListItem(self.folder_path)
