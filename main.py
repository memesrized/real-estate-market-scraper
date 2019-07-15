import sys
import browsers
import maps
import parsers
import processing
import pandas as pd

"""Apply pipleline and create required images."""

reg = sys.argv[1] 
size = sys.argv[2] # Num of instances for district hist.

# Crawl cian.ru and create .csv for each page
browser = browsers.CianBrowser('cian.ru',parser=parsers.CianParser,region=reg)
browser.crawl_pages_rooms(exit=True)
print('Crawled '+reg)

# Gather all files from previous step in one dataset
processing.assemble_dataset(folder=reg, save_path='cities')
print('Assembled '+reg)

# Check address and then try to correct mistakes.
# Correction includes reverse geocoding with Google maps API.
# So, you should first set it in config.
# Keep in output only lines with correct address after second check.
processing.correct_address(f'./cities/{reg}.csv', file_name=f'{reg}_correct_addr')
print('Corrected '+reg)

# Create interactive google map window with heatmap layer 
maps.save_map_html(f'./cities/{reg}.csv', reg)
print('html exported')

# Crawl 2GIS with selenium. 
# Re-create webdriver for every ~50 lines. 
# Note.
# Nothing lasts forever, except this function. 
# Don't forget to specify `size` param with small value.
# Approximate time for size=1000 is 6-7 minutes on my potato PC.
processing.append_district(f'./datasets/{reg}_correct_addr.csv',
                           save_path=f'./datasets/{reg}_distr_{size}.csv',
                           size=size,
                           region=reg)
print('District added')

# Plot hist for districts ('unknown' excluded)
df = pd.read_csv(f'./datasets/{reg}_distr_{size}.csv')
plot = df.loc[df['distr']!='unknown',['distr','weighted_price']].groupby('distr').agg('mean').plot.hist(bins=12)
fig = plot.get_figure()
fig.savefig(f'./cities/hist_price_{reg}.png')
print('Done!')