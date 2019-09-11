'''
author: Drew Cooper
date: April 16, 2019
'''

import os
import pandas as pd

from .base import Base
from .households import Households
from .persons import Persons
from .trips import Trips
from .vehicles import Vehicles
from .days import Days
from .locations import Locations

class Survey(object):
    def __init__(self, root=None, household_file=None, person_file=None,
                 vehicle_file=None, day_file=None, trip_file=None, location_file=None,
                 ):
        if household_file:
            self.households = Households(os.path.join(root, household_file))
        if person_file:
            self.persons = Persons(os.path.join(root, person_file))
        if trip_file:
            self.trips = Trips(os.path.join(root, trip_file))
        if day_file:
            self.days = Days(os.path.join(root, day_file))
        if vehicle_file:
            self.vehicles = Vehicles(os.path.join(root, vehicle_file))
        if location_file:
            self.locations = Locations(os.path.join(root, location_file))
        
        self.data_dictionary = self._create_data_dictionary()
        
    def _create_data_dictionary(self):
        d = dict(self.households.descriptions)
        d.update(self.persons.descriptions)
        d.update(self.trips.descriptions)
        d.update(self.days.descriptions)
        d.update(self.vehicles.descriptions)
        d.update(self.locations.descriptions)
        self.descriptions = d    
        
        v = dict(self.households.value_lookup)
        v.update(self.persons.value_lookup)
        v.update(self.trips.value_lookup)
        v.update(self.days.value_lookup)
        v.update(self.vehicles.value_lookup)
        v.update(self.locations.value_lookup)
        self.values = v
        
        dd = {}
        for k, v in self.descriptions.items():
            dd[k] = self._create_data_dictionary_entry(k, v, self.values[k] if k in self.values.keys() else None)
        return dd
            
    def _create_data_dictionary_entry(self, name, description, values=None):
        s = 'field name: {}\n\n'.format(name)
        s += 'description: {}\n\n'.format(description)
        if isinstance(values, dict):
            for k, v in values.items():
                s += '{:5}: {}\n'.format(k, v)
        return s
        
    def link_trips(self, linked_trip_id=None, sortby=None, groupby=None, change_mode_field=None, change_mode_value=None, mode_field=None):
        self._linked_trips = LinkedTrips(self.trips, 
                                         linked_trip_id,
                                         sortby,
                                         groupby,
                                         change_mode_field,
                                         change_mode_value,
                                         mode_field)
    
    def filter_by(self, filter_what, by_what, how):
        '''
        Manually filter one of the files and filter the rest based on it.
        '''
        raise NotImplementedError()
        
    def filter_complete_days(self):
        # TODO make this generic
        # get the trips for these persons for all days they completed
        self.days.data = self.days.data.loc[self.days.data['day_complete'].eq(1)]

        # get the records for these persons for all days they completed
        self.households.data = self.households.data.loc[self.households.data['hh_id'].isin(self.days.data['hh_id'])]
        self.persons.data = self.persons.data.loc[self.persons.data['person_id'].isin(self.days.data['person_id'])]
        self.trips.data = pd.merge(self.trips.data, self.days.data.loc[:,['hh_id','person_id','day_num','day_complete']])
        self.trips.data = self.trips.data.loc[self.trips.data['day_complete'].eq(1)]
        self.locations.data = self.locations.data.loc[self.locations.data['trip_id'].isin(self.trips.data['trip_id'])]
        
        
    def summarize(self, household_weights=None, person_weights=None, day_weights=None, trip_weights=None, human_readable=True, append=True):
        self.households.summarize(human_readable, household_weights, append)
        self.persons.summarize(human_readable, person_weights, append)
        self.days.summarize(human_readable, day_weights, append)
        self.trips.summarize(human_readable, trip_weights, append)
