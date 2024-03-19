"""This module contains a class definition for SongListItem"""

# pylint: disable=E0611
from os import listdir
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt

class SongListItem(QListWidgetItem):
    """
    Defines a SongListItem that additionally stores 
    metadata about the song folder it represents.
    """

    def __init__(self, path: str):
        super().__init__()

        self.setTextAlignment(Qt.AlignCenter)

        self.metadata = [] #List of all the metadata in the song's .osu
        self.folder_path = path
        self.folder_name = path.split("/")[-1]
        self.artist = ""
        self.artist_unicode = ""
        self.title = ""
        self.title_unicode = ""
        self.mapper = ""
        self.source = ""
        self.tags = ""

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
                self.metadata.append(word)

        self.setText(f"{self.artist} - {self.title}\nby {self.mapper}")

    def folder(self) -> str:
        """Return the name of the song's folder"""
        return self.folder_name

    def path(self) -> str:
        """Return the path to the folder"""
        return self.folder_path
