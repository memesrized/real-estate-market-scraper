import os
import pandas as pd

from abc import ABC, abstractmethod
from collections import defaultdict
from bs4 import BeautifulSoup

class CustomParser(ABC):
    """Abstract class for parsers"""
    def __init__(self, html, page_num=0, folder_name='csv_pages'):
        """
        Init
        
        self.flats -- dict with columns for datasets
        """
        self.page = BeautifulSoup(html, 'html.parser')
        self.flats = defaultdict(list)
        self.page_num = page_num
        self.folder_name = folder_name
        
    @abstractmethod    
    def collect_info(self):
        """Parse page into self.flats"""
        pass
                 
    def save_to_csv(self, prefix):
        """Save dict as csv
        
        prefix -- prefix for filename
        """
        df = pd.DataFrame(self.flats)
        if os.path.exists(self.folder_name):
            pass
        else:
            os.mkdir(self.folder_name)
        df.to_csv(f'./{self.folder_name}/{prefix}_page_{self.page_num}.csv',index=False)
        
class CianParser(CustomParser):
    
    """Parser ah hoc cian.ru"""
    
    def collect_info(self, save=True, prefix=''):
        adverts = self.page.find_all('tr', {'deal-type':'sale'})
        
        for ad in adverts:
            address = ad.find(class_='objects_item_info_col_1').find_all(class_='objects_item_addr')
            
            
            self.flats['address'].append(';'.join(map(lambda x: x.find('a').text, address)))
            
            #sometimes positions (town, district, street, house_number) are skewed by additional or absent points
            if len(address)>=4:    
                self.flats['district'].append(address[-3].find('a').text)
                self.flats['street'].append(address[-2].find('a').text)            
                self.flats['house_number'].append(address[-1].find('a').text)
            else:
                self.flats['district'].append('unknown')
                self.flats['street'].append('unknown')            
                self.flats['house_number'].append('unknown')      
            self.flats['coords'].append(ad.find('input')['value'])
            
            area = ad.find(class_='objects_item_info_col_3')
            self.flats['area'].append(float(area.find_all('td')[0].text.split('\xa0')[1].replace(',','.')))
            
            price = ad.find(class_='objects_item_info_col_4')
            temp = price.find('strong').text
            self.flats['full_price'].append(''.join([x for x in temp if x.isnumeric()]))
            temp = price.find_all('div')[3].text.split('-')[1]
            self.flats['weighted_price'].append(''.join([x for x in temp if x.isnumeric()]))
            
        if save:
            self.save_to_csv(prefix)
        else:
            return self.flats

