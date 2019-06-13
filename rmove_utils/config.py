'''
author: Drew Cooper
date: April 16, 2019
'''
import os
import pandas as pd

from rmove_utils.base import Base
from rmove_utils.households import Households
from rmove_utils.persons import Persons
from rmove_utils.trips import Trips
from rmove_utils.days import Days
from rmove_utils.vehicles import Vehicles
from rmove_utils.locations import Locations

class Config():
    # FIELD_COLUMNS = ['variable',
                     # 'data_type',
                     # 'description']
    FIELD_COLUMNS = ['variable']
    DATASET_TO_KEY = {'Households':'hh',
                      'Persons':'person',
                      'Vehicles':'vehicle',
                      'Days':'day',
                      'Trips':'trip',
                      'Locations':'loc',
                      }
                       
    def from_excel(path='.', 
                   config_file='2019-02-28_Bay_Area_TNC_Codebook.xlsx', 
                   fields_sheet_name='Overview', 
                   values_sheet_name='Values'):
        fkey = fields_sheet_name
        vkey = values_sheet_name
        config_dfs = pd.read_excel(os.path.join(path,config_file), 
                        [fields_sheet_name, values_sheet_name])

        Households.expected_columns = Config._read_expected_columns('Households', config_dfs[fkey])
        Persons.expected_columns = Config._read_expected_columns('Persons', config_dfs[fkey])
        Trips.expected_columns = Config._read_expected_columns('Trips', config_dfs[fkey])
        Days.expected_columns = Config._read_expected_columns('Days', config_dfs[fkey])
        Vehicles.expected_columns = Config._read_expected_columns('Vehicles', config_dfs[fkey])
        Locations.expected_columns = Config._read_expected_columns('Locations', config_dfs[fkey])
        
        Households.value_lookup = Config._read_value_lookup(Households.expected_columns, config_dfs[vkey])
        Persons.value_lookup = Config._read_value_lookup(Persons.expected_columns, config_dfs[vkey])
        Trips.value_lookup = Config._read_value_lookup(Trips.expected_columns, config_dfs[vkey])
        Days.value_lookup = Config._read_value_lookup(Days.expected_columns, config_dfs[vkey])
        Vehicles.value_lookup = Config._read_value_lookup(Vehicles.expected_columns, config_dfs[vkey])
        Locations.value_lookup = Config._read_value_lookup(Locations.expected_columns, config_dfs[vkey])
        
        Households.descriptions = Config._read_descriptions('Households', config_dfs[fkey])
        Persons.descriptions = Config._read_descriptions('Persons', config_dfs[fkey])
        Trips.descriptions = Config._read_descriptions('Trips', config_dfs[fkey])
        Days.descriptions = Config._read_descriptions('Days', config_dfs[fkey])
        Vehicles.descriptions = Config._read_descriptions('Vehicles', config_dfs[fkey])
        Locations.descriptions = Config._read_descriptions('Locations', config_dfs[fkey])
        
        Households.error_code_lookup = Config._read_value_lookup(['All categorical variables'], config_dfs[vkey])['All categorical variables']
        Persons.error_code_lookup = Config._read_value_lookup(['All categorical variables'], config_dfs[vkey])['All categorical variables']
        Trips.error_code_lookup = Config._read_value_lookup(['All categorical variables'], config_dfs[vkey])['All categorical variables']
        Days.error_code_lookup = Config._read_value_lookup(['All categorical variables'], config_dfs[vkey])['All categorical variables']
        Vehicles.error_code_lookup = Config._read_value_lookup(['All categorical variables'], config_dfs[vkey])['All categorical variables']
        Locations.error_code_lookup = Config._read_value_lookup(['All categorical variables'], config_dfs[vkey])['All categorical variables']
        
    def _read_expected_columns(dataset, df):
        df = df.loc[df[Config.DATASET_TO_KEY[dataset]].eq(1), Config.FIELD_COLUMNS]
        if len(Config.FIELD_COLUMNS) == 1:
            return df[Config.FIELD_COLUMNS[0]].tolist()
        return df.apply(lambda x: tuple(x[c] for c in Config.FIELD_COLUMNS), axis=1).tolist()
        
    def _read_value_lookup(expected_columns, df):
        df = df.loc[df['variable'].isin(expected_columns)]
        return {key: {v['value']: v['label'] for k, v in values.iterrows()} 
                    for key, values in df.groupby('variable')}
                    
    def _read_descriptions(dataset, df):
        df = df.loc[df[Config.DATASET_TO_KEY[dataset]].eq(1), :]
        return {row['variable']: row['description'] for idx, row in df.iterrows()} 
        