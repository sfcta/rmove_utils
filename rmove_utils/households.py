'''
author: Drew Cooper
date: April 16, 2019
'''

import os
import pandas as pd
import geopandas as gpd

from .base import Base
from .utils import point_in_polygon

class Households(Base):
    expected_columns = []
    value_lookup = {}
    
    def __init__(self, file_name=None, sep='\t', sort_by=None, error_level=0):
        super().__init__(file_name, sep, sort_by, error_level)
        self.home_x = None
        self.home_y = None
        
    def add_home_location(self, poly, field, name='home_location'):
        '''
        TODO: Testing needed.
        poly: a GeoDataFrame of polygons
        field: the field name in poly to assign to home_location
        '''
        home = gpd.GeoDataFrame(index=self.data.index, 
                                geometry=self.data.apply(lambda x: Point(x[self.home_x],x[self.home_y]),
                                                         axis=1))
        self.data[name] = point_in_polygon(home, poly, field)