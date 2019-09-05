'''
author: Drew Cooper
date: July 24, 2019
'''

import os
import numpy as np
import pandas as pd

from .base import Base
from .trips import Trips

class LinkedTrips(Trips):
    expected_columns = []
    value_lookup = {}
    crs = None
    
    def __init__(self, file_name=None, sep='\t', error_level=0):
        if file_name != None:
            super().__init__(file_name, sep, error_level)
            
        self._geos = {}
    
    def link_trips(grouped_unlinked_trips, mode, modes, mode_heirarchy):
        # first get the main mode
        for m in mode_heirarchy:
            if m in grouped_unlinked_trips[mode].tolist():
                break 
                
        if len(grouped_unlinked_trips) > 1:
            access_mode = grouped_unlinked_trips[mode].iloc[0]
            egress_mode = grouped_unlinked_trips[mode].iloc[-1]
        has_mode = []
        
        for m in modes:
            has_mode.append(1 if m in grouped_unlinked_trips[mode].tolist() else 0)
            

        
        # TODO
        #iwait = 
        #xwait = 
        #ivtt = 
        #vmt = 
        
        return pd.Series(index=['mode','access_mode','egress_mode']+['has_mode_{:d}'.format(m) for m in modes],
                         data=[m, access_mode, egress_mode]+has_mode,
                         )
    
    @classmethod
    def from_file(cls, file_name=None, sep='\t', error_level=0):
        return cls(file_name=file_name, sep=sep, error_level=error_level)
        
    @classmethod
    def from_trips(cls, trips, linked_trip_id=None, sortby=None, groupby=None, change_mode_field=None, change_mode_value=None, 
                   mode_field=None, modes=None, mode_heirarchy=None):
        '''
        Creates a LinkedTrips from a Trips object or a trips dataframe.  Must supply linked_trip_id or
            change_mode_field and change_mode_key.  
            
        `linked_trip_id`: an id that designates a set of unlinked trips that are related as a linked trip
        
        `other_link_id`:
        
        `change_mode_field`: the field that indicates whether the trip purpose is to change modes using
            the `change_mode_value`.
        
        `change_mode_value`: the value in `change_mode_field` that indicates that the trip purpose is to
            change modes.
        
        `sortby`: column or columns to sort by.  If none is provided, then the order is assumed to be as-is.
        '''
        
        if isinstance(trips, Trips):
            self.expected_columns=trips.expected_columns
            self.value_lookup=trips.value_lookup
            self.crs=trips.crs
            self.descriptions=trips.descriptions
            self.error_code_lookup=trips.error_code_lookup
            trips=trip.data.copy()
        elif isinstance(trips, pd.DataFrame):
            pass
        else:
            print(trips)
            raise TypeError('Unrecognized type: {}'.format(type(trips)))
            
        if sortby:
            trips.sort_values(sortby, inplace=True)
            
        if linked_trip_id:
            raise NotImplementedError()
            
        else:
            linked_trip_id='linked_trip_id'
            trips['linked_trip_id'] = np.nan
            
            (trips
             .loc[trips[change_mode_field]
                  .ne(change_mode_value),
                  linked_trip_id]) = np.arange(1, len(trips.loc[trips[change_mode_field].ne(change_mode_value)])+1)
            
            trips['linked_trip_id'] = trips['linked_trip_id'].bfill()  
            
            self.data = trips.groupby(groupby+[linked_trip_id]).apply(lambda x: LinkedTrips.link_trips(x, mode_field, modes, mode_heirarchy))
            
    
        