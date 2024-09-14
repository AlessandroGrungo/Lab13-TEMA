import math
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

    def distance_HV(self, other) -> float:
        """
        Function that calculate the approximate geodesic distance between two sightings.
        :param other: another sighting.
        :return: the approximate geodesic distance in kilometers
        """
        lat1 = self._Lat * math.pi / 180
        lon1 = self._Lng * math.pi / 180
        lat2 = other._Lat * math.pi / 180
        lon2 = other._Lng * math.pi / 180
        R = 6371  # earth radius in km
        a = math.sin(0.5 * (lat2 - lat1)) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(0.5 * (lon2 - lon1)) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c