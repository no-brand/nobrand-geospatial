# -*- coding: utf-8 -*-

import unittest
from geospatial import *
from decimal import *


class LatLngTestCase(unittest.TestCase):

    def setUp(self):
        self.longitude = 127.0712703
        self.latitude = 37.2874104
        self.latlng = LatLng(longitude=Decimal(self.longitude), latitude=Decimal(self.latitude))

    def test_s2hash(self):
        s2hash = self.latlng.geohash()
        expected = '3853774061772425397'
        self.assertEqual(s2hash, expected)
        self.assertEqual(len(s2hash), len(expected))

    def test_geohash(self):
        geohash = self.latlng.geohash32()
        expected = 'wydk5efqzjnd'
        self.assertEqual(geohash, expected)
        self.assertEqual(len(geohash), len(expected))

    def test_geojson(self):
        geojson = self.latlng.geojson
        expected = {'type': 'Point', 'coordinates': [self.longitude, self.latitude]}
        self.assertEqual(geojson, expected)

    def test_serialize_to_elastic(self):
        dic = self.latlng.serialize_to_elastic()
        for key in ['longitude', 'latitude']:
            self.assertIn(key, dic.keys())
            self.assertTrue(isinstance(dic[key], float))
        for key in ['geohash', 'geohash32']:
            self.assertIn(key, dic.keys())
            self.assertTrue(isinstance(dic[key], str))
        for key in ['location']:
            self.assertTrue(isinstance(dic[key], dict))
            self.assertEqual(dic[key]['lon'], self.longitude)
            self.assertEqual(dic[key]['lat'], self.latitude)

    def test_serialize_to_ddb(self):
        dic = self.latlng.serialize_to_ddb()
        for key in ['longitude', 'latitude']:
            self.assertIn(key, dic.keys())
            self.assertTrue(isinstance(dic[key], Decimal))
        for key in ['hashKey', 'geohash', 'hashKey32', 'geohash32', 'geoJson']:
            self.assertIn(key, dic.keys())
            self.assertTrue(isinstance(dic[key], str))

    def test_serialize_to_ddb_nested(self):
        dic = self.latlng.serialize_to_ddb(type_nested=True)
        for key in ['longitude', 'latitude']:
            self.assertIn(key, dic.keys())
            self.assertIn('N', dic[key])
        for key in ['hashKey', 'geohash', 'hashKey32', 'geohash32', 'geoJson']:
            self.assertIn(key, dic.keys())
            self.assertIn('S', dic[key])


if __name__ == '__main__':
    unittest.main()
