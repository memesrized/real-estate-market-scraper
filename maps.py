import sys
import yaml
import gmaps
import pandas as pd

from ipywidgets.embed import embed_minimal_html

"""Create map and save it as html"""

def save_map_html(path_to_csv, file_name):
    """Create map and save it as html
    
    Be sure that config is created.
    (required Google maps api_key with JavascriptAPI)
    
    path_to_csv -- file with data
    file_name -- name of html file
    """
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)    
    gmaps.configure(api_key=config['API_key'])
    
    median_price = pd.read_csv(path_to_csv)
    locations = median_price[['lat', 'lon']]
    weights = median_price['weighted_price']
    fig = gmaps.figure()
    fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
    embed_minimal_html(f'{file_name}.html', views=[fig])

if __name__=='__main__':
    save_map_html(sys.argv[1], sys.argv[2])

