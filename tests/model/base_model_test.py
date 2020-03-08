# -*- coding: utf-8 -*-

import unittest
from geospatial import *


class BaseModelTestCase(unittest.TestCase):

    def test_abstract_base_class_initiation(self):
        with self.assertRaises(TypeError):
            BaseModel()


if __name__ == '__main__':
    unittest.main()
