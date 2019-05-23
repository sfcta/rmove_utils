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
        
        
        