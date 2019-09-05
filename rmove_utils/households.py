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
    expected_columns = ['hhid',
                      'sample_segment',
                      'sample_stratum',
                      'sample_address',
                      'sample_home_lat',
                      'sample_home_lon',
                      'home_lat',
                      'home_lon',
                      'travel_date_start',
                      'travel_date_end',
                      'hhsize',
                      'num_vehicles',
                      'num_workers',
                      'income_detailed',
                      'income_followup',
                      'income_aggregate',
                      'rent_own',
                      'res_duration',
                      'res_type',
                      'res_months',
                      'required_demographics_complete',
                      'hh_num_days_complete',
                      'hh_num_trips',
                      'hh_tnc_trips',
                      'hh_shared_mobility_trips']
              
    value_lookup = {'sample_segment':{1: 'San Francisco', 
                                      2: 'Eight County'},
                    'sample_stratum':{1: 'SF - Very High TNC',
                                      2: 'SF - High TNC',
                                      3: 'SF - Medium TNC',
                                      4: 'SF - General Population',
                                      5: 'Eight County - Very High TNC',
                                      6: 'Eight County - High TNC',
                                      7: 'Eight County - Medium TNC',
                                      8: 'Eight County - General Population'},
                     }

    
    def __init__(self, file_name=None, sep='\t', error_level=0):
        super().__init__(file_name, sep, error_level)
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