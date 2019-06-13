'''
author: Drew Cooper
date: April 16, 2019
'''

import os
import itertools
import pandas as pd

class Base(object):
    expected_columns = []
    value_lookup = {}
    descriptions = {}
    error_code_lookup = {}
    
    def __init__(self, file_name=None, sep='\t', error_level=0):
        self.data = pd.read_csv(file_name, sep)
        
        if isinstance(self.expected_columns[0], tuple):
            expected_columns = []
            for c in self.expected_columns:
                expected_columns.append(c)
        else:
            expected_columns = self.expected_columns
        
        self._validate_columns(error_level)
        self._validate_values(error_level)
            
    def _validate_columns(self, error_level):
        for col in self.data.columns:
            if col not in self.expected_columns:
                if error_level==0:
                    print('found unexpected column {} in {}.'.format(col, type(self)))
                elif error_level==1:
                    raise('found unexpected column {} in {}.'.format(col, type(self)))
                
        for col in self.expected_columns:
            if col not in self.data.columns:
                if error_level==0:
                    print('did not find expected column {} in {}.'.format(col, type(self)))
                elif error_level==1:
                    raise('did not find expected column {} in {}.'.format(col, type(self)))
    
    def _validate_values(self, error_level):
        for col in self.data.columns:
            if col in self.expected_columns and col in self.value_lookup.keys():
                for k, v in self.data.groupby(col).size().items():
                    if k not in itertools.chain(self.value_lookup[col].keys(),
                                self.error_code_lookup.keys()):
                        if error_level==0:
                            print('found {} unexpected value(s) {} for column {} in {}.'.format(v, k, col, type(self)))
                        if error_level==1:
                            raise('found {} unexpected value(s) {} for column {} in {}.'.format(v, k, col, type(self)))
                    
                
    def human_readable(self):
        df = self.data.copy()
        for key, values in self.value_lookup.items():
            values.update(self.error_code_lookup)
            try:
                df[key] = df[key].map(lambda x: values[x])
            except Exception as e:
                print('error converting values in columns {} of {} to human readable form.'.format(key, type(self)))
                print(e)
        return df