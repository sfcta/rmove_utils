'''
author: Drew Cooper
date: April 16, 2019
'''

import os
import pandas as pd

from .base import Base

class Vehicles(Base):
    expected_columns = []
    value_lookup = {}
    
    def __init__(self, file_name=None, sep='\t', sort_by=None, error_level=0):
        super().__init__(file_name, sep, sort_by, error_level)
