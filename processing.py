import itertools
import os
import re
import time
import yaml
import numpy as np
import pandas as pd

from geopy.geocoders import GoogleV3
from pandas.errors import EmptyDataError

from browsers import GisBrowser

"""Data processing functions"""

def assemble_dataset(folder='spb', save_path='datasets', save=True):
    """Gather info from set of csv
    
    folder -- folder with set of csv
    save_path -- folder for output
    """
    csvs = os.listdir(f'./{folder}')
    df = pd.DataFrame()
    for csv in csvs:
        try:
            df = pd.concat([pd.read_csv(f'./{folder}/{csv}'),df])
        except EmptyDataError:
            continue
    df.reset_index(drop=True, inplace=True)
    df['lat'] = df['coords'].map(lambda x: x.split(',')[0])
    df['lon'] = df['coords'].map(lambda x: x.split(',')[1])
    
    if save:
        if os.path.exists(save_path):
            pass
        else:
            os.mkdir(save_path)
        df.to_csv(f'./{save_path}/{folder}.csv', index=False)
    else:
        return df
    
def correct_address(df, file_name='correct_address', save_path='datasets', save=True):
    """Correct inappropriate address
    
    df -- data (string path or dataframe)
    
    Be sure that config is created.
    (required Google maps api_key with GeocoderAPI)
    """
    
    if type(df).__name__ == 'str':
        df = pd.read_csv(df)
    
    # Pattern to check 
    pattern = re.compile("^(д.)\s*[0-9а-яА-Я]*")
    df['is_correct'] = df['house_number'].map(lambda x: 1 if pattern.match(x) else 0)
    incorrect_address = df.loc[df['is_correct']==0]
    
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    
    #Reverse geocoding
    geolocator = GoogleV3(api_key=config['API_key'], domain='maps.google.ru')
    reversed_coords = incorrect_address['coords'].apply(lambda x: geolocator.reverse(x, exactly_one=True)).to_list()
    
    incorrect_address['street'] = list(map(lambda x: x[0].split(',')[0],reversed_coords))
    incorrect_address['house_number'] = list(map(lambda x: x[0].split(',')[1],reversed_coords))
    
    #Insert correct address
    for i in incorrect_address.index:
        df.loc[i,'street'] = incorrect_address.loc[i,'street']
        df.loc[i,'house_number'] = incorrect_address.loc[i,'house_number']

    pattern = re.compile("[а-яА-Я]*.*\s*[0-9]+/*[0-9а-яА-Я]*")
    #Second check
    df['is_correct'] = df['house_number'].map(lambda x: 1 if pattern.match(x) else 0)
    
    if save:
        if os.path.exists(save_path):
            pass
        else:
            os.mkdir(save_path)
        df.to_csv(f'./{save_path}/{file_name}.csv', index=False)
    else:
        return df
    
def get_districts(addr_list, location):
    """Return list of districts"""
    temp_streets = []
    
    # Split is necessary, it starts to lag when working too long.
    # Re-create browser for ~50 elements
    for array in np.array_split(addr_list,len(addr_list)//50):
        try:
            temp = GisBrowser(location=location)
            temp_streets.append(temp.get_districts(array))
        except:
            print(f'Exception on {array[0]} - {array[-1]}')
            return list(itertools.chain.from_iterable(temp_streets))
    return list(itertools.chain.from_iterable(temp_streets))

def append_district(df_path, save_path, size, region):
    """Append district (okrug) to dataset and save it.
    
    Only lines with correct address is chosen.
    """
    df = pd.read_csv(df_path)
    df = df.loc[df['is_correct']==1].reset_index(drop=True)
    df = df.loc[:size]
    regions = {'msk':'Москва', 'spb':'Санкт-Петебург', 'ekb':'Екатеринбург'}
    # Region is necessary because of answer structure
    list_of_streets = df['street'].map(lambda x: f'{regions[region]} '+x+' ')+df['house_number']
    temp = get_districts(list_of_streets, region)
    try:
        df['distr'] = temp
    except:
        return temp
    df.to_csv(save_path, index=False)
    

