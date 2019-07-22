import geopandas as gpd

def point_in_polygon(points, polygons, name_field):
    if not points.crs:
        points.crs = {'init':'epsg:4326'}
    points = points.to_crs(polygons.crs)
    s = gpd.sjoin(points, polygons)
    return s[name_field]
    
def ethnicity(row, descriptions, values):
    if row['ethnicity_no_answer'] == 1:
        return 'No Answer'
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
        return 'Multi'
    if row[['ethnicity_af_am','ethnicity_aiak','ethnicity_asian','ethnicity_hapi','ethnicity_hisp','ethnicity_white','ethnicity_other']].sum() == 1:
        for x in ['ethnicity_af_am','ethnicity_aiak','ethnicity_asian','ethnicity_hapi','ethnicity_hisp','ethnicity_white','ethnicity_other']:
            if row[x] == 1:
                return descriptions[x].replace('Ethnicity: ', '')
    if row[['ethnicity_af_am','ethnicity_aiak','ethnicity_asian','ethnicity_hapi','ethnicity_hisp','ethnicity_white','ethnicity_other']].eq(1).any():
        return 'Multi'
    return 'exception'
    
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