'''
author: Drew Cooper
date: April 16, 2019
'''

import os
import pandas as pd

from .base import Base

class Trips(Base):
    expected_columns = []
    value_lookup = {}
    crs = None
    
    
    def __init__(self, file_name=None, sep='\t', error_level=0):
        super().__init__(file_name, sep, error_level)
        self._geos = {}
        
    def add_geography(self, geog_file, x_col='o_lon', y_col='o_lat', geo_col=None, name='o_taz', data_crs=None, geog_crs=None):
        if not data_crs and self.crs:
            data_crs = self.crs
        self._add_geoseries(x_col, y_col, geo_col, data_crs, name)
        return
        #projected = self._geos
    
    def _add_geoseries(self, x_col=None, y_col=None, geo_col=None, crs=None, name=None):
        '''
        Create a geoseries and store it in self._geos with the key `name`.
        
        Requires both x_col and y_col or requires coord_col, but 
        not all three.  If x_col and y_col, then the column values must be of
        data type float. If geo_col is supplied, then it must contain a Point
        object or a tuple of (x, y) where x and y are floats.
        '''
        import geopandas as gpd
        from shapely.geometry import Point
        
        if (x_col==None and y_col==None) != (geo_col==None):
            raise('supply both x_col and y_col, or supply geo_col')
        
        if x_col and y_col:
            if not name:
                name = x_col + '_' + y_col
            #if isinstance(
            self._geos[name] = gpd.GeoSeries(
                index=self.data.index, 
                geometry=self.data.apply(lambda x: Point(x[x_col], x[y_col]), axis=1)
                )
        else:
            if not name:
                name = geo_col
            self._geos[name] = gpd.GeoSeries(
                index=self.dta.index,
                geometry=self.data[geo_col].map(lambda x: Point(x))
                )