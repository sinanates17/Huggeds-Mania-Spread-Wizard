"""This module contains class definition for GraphData and StrainObject"""

#from Statistician.note import Hand

class StrainObject:
    """Contains a value, timestamp, and hand. A glorified tuple."""

    def __init__(self, value: float, timestamp: int, hand):
        self.value = value
        self.timestamp = timestamp
        self.hand = hand #From the Hand Enum in the note module

class RawGraphData:
    """A glorified StrainObject container."""

    def __init__(self, name):
        self._name = name
        self._points = []

    def __repr__(self) -> str:
        return self._name

    def add_point(self, point: StrainObject):
        """Adds a StrainObject to the list of point."""

        self._points.append(point)

    def points(self) -> list[StrainObject]:
        """Returns the list of StrainObjects"""

        return self._points

    def clear(self):
        """Clear all strain points."""

        self._points.clear()
