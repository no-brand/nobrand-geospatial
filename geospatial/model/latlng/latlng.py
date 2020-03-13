# -*- coding: utf-8 -*-

from ..base_model import *
import s2sphere as s2
import pygeohash as gh


class LatLng(BaseModel):
    def __init__(self, longitude: Decimal, latitude: Decimal):
        self.longitude = float(longitude)
        self.latitude = float(latitude)
        self.__geohash = self.set_geohash(self.latitude, self.longitude)
        self.__geohash32 = self.set_geohash32(self.latitude, self.longitude)
        self.__geojson = {
            "type": "Point",
            "coordinates": [self.longitude, self.latitude]
        }

    @staticmethod
    def set_geohash(lat, lon):
        latlng = s2.LatLng.from_degrees(lat, lon)
        cell = s2.CellId.from_lat_lng(latlng)
        return str(cell.id())

    @staticmethod
    def set_geohash32(lat, lon):
        return gh.encode(lat, lon)

    def geohash(self, precision=19):
        return self.__geohash[:precision]

    def geohash32(self, precision=12):
        return self.__geohash32[:precision]

    @property
    def geojson(self):
        return self.__geojson

    def __dict__(self):
        return {
            'longitude': self.longitude,
            'latitude': self.latitude,
            'geohash': self.geohash(),
            'geohash32': self.geohash32(),
            'hashKey': self.geohash(precision=5),
            'hashKey32': self.geohash32(precision=7),
            'geoJson': self.geojson
        }

    def prepare_serialize_to_ddb(self, params=None):
        assert params is not None
        params['geoJson'] = json.dumps(params['geoJson'])
        return params

    def prepare_serialize_to_elastic(self, params=None):
        assert params is not None
        params['location'] = {
            'lon': params['longitude'],
            'lat': params['latitude']
        }
        for key in ['hashKey', 'hashKey32', 'geoJson']:
            del params[key]
        return params
