
from dataclasses import dataclass
from datetime import datetime
@dataclass
class State:
    _id: int
    _Name: str
    _Capital: str
    _Lat: float
    _Lng: float
    _Area: float
    _Population: int
    _Neighbors: []

    @property
    def id(self):
        return self._id
    @property
    def lat(self):
        return self._Lat
    @property
    def lng(self):
        return self._Lng
    @property
    def Name(self):
        return self._Name

    def __str__(self):
        return self._Name

    def __hash__(self):
        return hash(self._id)
