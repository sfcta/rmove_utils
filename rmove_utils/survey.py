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
            self._households = Households(os.path.join(root, household_file))
            self.households = self._households.human_readable()
        if person_file:
            self._persons = Persons(os.path.join(root, person_file))
            self.persons = self._persons.human_readable()
        if trip_file:
            self._trips = Trips(os.path.join(root, trip_file))
            self.trips = self._trips.human_readable()
        if day_file:
            self._days = Days(os.path.join(root, day_file))
            self.days = self._days.human_readable()
        if vehicle_file:
            self._vehicles = Vehicles(os.path.join(root, vehicle_file))
            self.vehicles = self._vehicles.human_readable()
        if location_file:
            self._locations = Locations(os.path.join(root, location_file))
            self.locations = self._locations.human_readable()
        
        self.data_dictionary = self._create_data_dictionary()
        
    def _create_data_dictionary(self):
        d = dict(self._households.descriptions)
        d.update(self._persons.descriptions)
        d.update(self._trips.descriptions)
        d.update(self._days.descriptions)
        d.update(self._vehicles.descriptions)
        d.update(self._locations.descriptions)
        self.descriptions = d    
        
        v = dict(self._households.value_lookup)
        v.update(self._persons.value_lookup)
        v.update(self._trips.value_lookup)
        v.update(self._days.value_lookup)
        v.update(self._vehicles.value_lookup)
        v.update(self._locations.value_lookup)
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
        
    def summarize(self, household_weights=None, person_weights=None, day_weights=None, trip_weights=None, human_readable=True, append=True):
        self._households.summarize(human_readable, household_weight, append)
        self._persons.summarize(human_readable, person_weight, append)
        self._days.summarize(human_readable, day_weight, append)
        self._trips.summarize(human_readable, trip_weight, append)