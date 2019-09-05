import geopandas as gpd

def point_in_polygon(points, polygons, name_field):
    if not points.crs:
        points.crs = {'init':'epsg:4326'}
    points = points.to_crs(polygons.crs)
    s = gpd.sjoin(points, polygons)
    return s[name_field]
    
def ethnicity(row, descriptions, values):
    '''
    Impute an race/ethnicity based on responses for each race/ethnicity field
    '''
    error_values = [-9998, 995, 999]
    eth = ''
    err = ''
    
    # first check if they're all an error
    # if any of them have an error code, then all of them do
    for ev in error_values:
        if row[['ethnicity_af_am','ethnicity_aiak','ethnicity_asian',
                'ethnicity_hapi','ethnicity_hisp','ethnicity_white',
                'ethnicity_other','ethnicity_multi']].eq(ev).all():
            return values['ethnicity_af_am'][ev]
                    
    # If no answer, return no answer
    if (row['ethnicity_no_answer'] == 1 or 
        row[['ethnicity_af_am','ethnicity_aiak','ethnicity_asian',
             'ethnicity_hapi','ethnicity_hisp','ethnicity_white',
             'ethnicity_other','ethnicity_multi']].eq(0).all()):
        return 'No Answer'
    
    # Now impute a racial/ethnic category from valid responses
    if (row['ethnicity_white'] == 1 and not
        row[['ethnicity_af_am','ethnicity_aiak',
             'ethnicity_asian','ethnicity_hapi',
             'ethnicity_hisp','ethnicity_other',
             'ethnicity_multi']].eq(1).any()):
        return 'White Non-Hispanic'
    if (row['ethnicity_hisp'] == 1 and not
        row[['ethnicity_af_am','ethnicity_aiak',
             'ethnicity_asian','ethnicity_hapi',
             'ethnicity_other','ethnicity_multi']].eq(1).any()):
        return 'White Hispanic'
    if row['ethnicity_multi'] == 1 :
        return 'Multiple'
    if row[['ethnicity_af_am','ethnicity_aiak','ethnicity_asian',
            'ethnicity_hapi','ethnicity_hisp','ethnicity_white',
            'ethnicity_other']].sum() == 1:
        for x in ['ethnicity_af_am','ethnicity_aiak','ethnicity_asian',
                  'ethnicity_hapi','ethnicity_hisp','ethnicity_white',
                  'ethnicity_other']:
            if row[x] == 1:
                return descriptions[x].replace('Ethnicity: ', '')
    if row[['ethnicity_af_am','ethnicity_aiak','ethnicity_asian',
            'ethnicity_hapi','ethnicity_hisp','ethnicity_white',
            'ethnicity_other']].sum() > 1:
        return 'Multiple'
    
    raise Exception('Could not impute race/ethnicity for {}'.format(row[['ethnicity_af_am','ethnicity_aiak',
                         'ethnicity_asian','ethnicity_hapi',
                         'ethnicity_hisp','ethnicity_other',
                         'ethnicity_multi']]))
    
def ethnicity_simple(row, descriptions, values):
    if row['ethnicity_no_answer'] == 1:
        return 'No Answer'
    if (row['ethnicity_white'] == 1 and not
        row[['ethnicity_af_am','ethnicity_aiak',
             'ethnicity_asian','ethnicity_hapi',
             'ethnicity_hisp','ethnicity_other',
             'ethnicity_multi']].eq(1).any()):
        return 'White Non-Hispanic'
    if row[['ethnicity_af_am','ethnicity_aiak','ethnicity_asian','ethnicity_hapi','ethnicity_hisp','ethnicity_other','ethnicity_multi']].eq(1).any():
        return 'All other races/ethnicities'
    return 'exception'
    
def ethnicity_medium(row, descriptions, values):
    if row['ethnicity_no_answer'] == 1:
        return 'No Answer'
    if (row['ethnicity_white'] == 1 and not
        row[['ethnicity_af_am','ethnicity_aiak',
             'ethnicity_asian','ethnicity_hapi',
             'ethnicity_hisp','ethnicity_other',
             'ethnicity_multi']].eq(1).any()):
        return 'white non-hispanic'
    if (row['ethnicity_hisp'] == 1 and not
        row[['ethnicity_af_am','ethnicity_aiak',
             'ethnicity_asian','ethnicity_hapi',
             'ethnicity_other','ethnicity_multi']].eq(1).any()):
        return 'white hispanic'
    if (row['ethnicity_multi'] == 1 or 
        row[['ethnicity_af_am','ethnicity_aiak',
             'ethnicity_asian','ethnicity_hapi',
             'ethnicity_other']].sum() > 1):
        return 'multi'
    if row['ethnicity_af_am'] == 1:
        return 'african american'
    if row['ethnicity_hapi'] == 1:
        return 'hawaiian or pacific islander'
    if row[['ethnicity_aiak','ethnicity_asian','ethnicity_other']].eq(1).any():
        return 'all other races/ethnicities'
    return 'exception'