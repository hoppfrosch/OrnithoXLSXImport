# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys
import os
import collections
from osgeo import gdal
from osgeo import ogr
from osgeo import osr

import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from OrnithoXLSXColumnDefinition import OrnithoXLSXColumnDefinition

__version__ = "0.1.0alpha02"


class OrnithoGeopackage:
    """Geopackage to hold data from Ornitho"""

    def __init__(self, pathGPKG, epsg=4226, overwrite=0):
        # print(int(gdal.VersionInfo('VERSION_NUM')))

        if int(gdal.VersionInfo('VERSION_NUM')) < 2020000:
            raise Exception('Geopackage requires GDAL >= 2.2')

        self.srs = osr.SpatialReference()
        self.srs.ImportFromEPSG(epsg)

        cwd = os.getcwd()
        path, file = os.path.split(pathGPKG)
        # Now change the directory
        os.chdir(path)

        self.driver = ogr.GetDriverByName('GPKG')

        if (os.path.exists(pathGPKG)):
            if (os.path.isfile(pathGPKG)):
                if (overwrite):
                    self.driver.DeleteDataSource(file)
                    self.dataSource = self.driver.CreateDataSource(file)
                else:
                    self.dataSource = self.driver.Open(file, 1)
            else:
                self.dataSource = self.driver.CreateDataSource(file)

        os.chdir(cwd)

    def layerCount(self):
        """get the count of layers within gpkg"""
        layerCount = self.dataSource.GetLayerCount()
        return layerCount

    def layerExists(self, layername):
        """Checks whether a layer given by name exists"""
        layerList = self.layerList()
        if layername:
            if layername in layerList:
                return True

    def layerList(self):
        """Get names of all layers in current geopackage"""
        layerList = []

        for i in range(0, self.layerCount()):
            daLayer = self.dataSource.GetLayerByIndex(i)
            if daLayer:
                daName = daLayer.GetName()
                if not daName in layerList:
                    layerList.append(daName)

        layerList.sort()
        return layerList
