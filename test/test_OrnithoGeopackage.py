# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'hoppfrosch@gmx.de'
__date__ = '2018-07-19'
__copyright__ = 'Copyright 2018, Johannes Kilian'

import unittest

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from OrnithoGeopackage import OrnithoGeopackage


class OrnithoGeopackageTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        self.gpkg = OrnithoGeopackage(
            "w:\Develop\OrnithoXLSXmporter\Data\jok_test_new2.gpkg")
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_layercount(self):
        """Test layercount."""
        layercount = self.gpkg.layerCount()
        self.assertEqual(layercount, 1)

    def test_layername(self):
        """Test layername."""
        layerlist = self.gpkg.layerList()
        res = False
        if 'ornitho' in layerlist:
            res = True
        self.assertEqual(res, True)

    def test_layerexists(self):
        """Test whether layer exists."""
        layerexists = self.gpkg.layerExists("ornitho")
        self.assertEqual(layerexists, True)


if __name__ == "__main__":
    suite = unittest.makeSuite(OrnithoGeopackageTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
