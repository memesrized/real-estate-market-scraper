import time

from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

"""Classes-wrappers for selenium webdriver."""

class CustomBrowser(ABC):
    
    """Abstract browser-class with basic operations.
    
    Used to collect datasets.
    """
    
    def __init__(self, main_page, parser, region='spb'):
        """Init instance.
        
        parser -- ad hoc html parser (saves csv)
        region -- spb/msk/ekb
        """
        self.driver = webdriver.Firefox()
        self.main_page = main_page
        self.region = self.encode_region(region)
        self.region_name = region
        self.current_page = 1
        self.parser = parser
        self._query = self.get_query()
        
    def goto_main_page(self):
        self.driver.get(f'https://{main_page}')
        
    @abstractmethod    
    def encode_region(self, region):
        """Create dict with regions.
        
        Because every site has its own codes for regions.
        """
        pass
    
    #TODO: put in `region` and `num_rooms` setters 
    @abstractmethod
    def get_query(self):
        """Specify url query for site."""
        pass
    
    def get_current_page(self):
        return self.driver.page_source
    
    @abstractmethod
    def get_next_page(self):
        """Move to next page (include query) and return its html"""
        pass
        
    def crawl_pages(self, parser, prefix='', max_range=100, exit=False):
        """Iterate through a list of pages reachable with query.
        
        Save every page in separate csv.
        
        parser -- ad hoc html parser (saves csv)
        prefix -- prefix for csv filename
        max_range -- num of pages to parse
        exit -- condition to close driver
        
        max_range can exceed real num of reachable pages.
        """
        self.current_page = 0
        for i in range(1,max_range+1):
            try:
                html = self.get_next_page()
                soup = self.parser(html, page_num=self.current_page, folder_name=self.region_name)
                soup.collect_info(prefix=prefix)
            except WebDriverException:
                break
        if exit:
            self.exit()
                
    def exit(self):
        """Close browser"""
        self.driver.quit()

class CianBrowser(CustomBrowser):
    
    """Browser for cian.ru"""
    
    def __init__(self, main_page, parser, region='spb'):     
        self.num_rooms = 1
        self.default_query = 'cat.php?deal_type=sale&engine_version=2&offer_type=flat'
        super().__init__(main_page, parser, region)
        
        #~~~kostyling~~~ below
        
        self.driver.get(f'https://{self.main_page}/{self.default_query}&p=1&region={self.region}')
        try:
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div[2]/div/noindex/a[3]').click()
        except:
            self.driver.find_elements_by_class_name('_93444fe79c--tab--1rznU')[1].click()
        self.driver.get(f'https://{self.main_page}/{self.default_query}&p=2&region={self.region}')
        self.driver.get(f'https://{self.main_page}/{self.default_query}&p=1&region={self.region}')
    
    def get_next_page(self):
        self.current_page += 1 
        self.driver.get(f'https://{self.main_page}/{self._query}&p={self.current_page}')
        return self.driver.page_source
    
    def encode_region(self, region):
        regions = {'msk':1, 'spb':2, 'ekb':4743}
        return regions[region]
    
    def get_query(self):
        return f'{self.default_query}&region={self.region}&room{self.num_rooms}=1'
                
    def crawl_pages_rooms(self, exit=False):
        """Collect info for flats with different num of rooms.
        
        There is restriction with only 30 pages for query.
        So for more info we should use different filters on query.
        The easiest approach is to change num of rooms.
        """
        for i in range(1,9):
            self.num_rooms = i
            self._query = self.get_query()
            self.crawl_pages(self.parser, prefix=str(i))
        if exit:
            self.exit()   
            
def DomofondBrowser(CustomBrowser):
    
    """Browser for domofond.ru
    
    Unused. Need to write a parser.
    """
    #ya ne uspel ewe prikrutit'  neskolko saitov(((((((((((((
    #pochti vse vremya ubil na okruga i 2gis ='(
    #poshadite
    def encode_region(self, region):
        regions = {'msk':'moskva-c3584','spb':'sankt_peterburg-c3414','ekb':'ekaterinburg-c2653'}
        return regions[region]
    
    def get_next_page(self):
        self.current_page += 1
        self.driver.get(f'https://{self.main_page}/{self._query}?Page={self.current_page}')
        return self.driver.page_source
    
    def get_query():
        return f'prodazha-kvartiry-{self.region}'

class GisBrowser():
    
    """2GIS browser
    
    Used to get districts (municipal'nye okruga, i mean) names
    for street names.
    """
    
    def __init__(self, location='spb'):
        self.driver = webdriver.Firefox()
        self.location = location
        self.driver.get(f'https://{location}.2gis.ru')
    
    def get_district(self, street):
        """Return district name by street name.
        
        Search street name with search bar and then
        try to parse dropped card with result.
        
        Note: There are no district names in Moscow, 
        you will get street name as result.
        """
        
        self.driver.get(f'https://2gis.ru/query/{street}')
        input_ = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div/div[1]/div/form/div[1]/div/div/input')
        #input_.send_keys(street)
        input_.send_keys(Keys.ENTER)
        
        try:
            card = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "cardFeatures__item")))
            card = self.driver.find_element_by_class_name('cardFeatures__item') 
            class_ = '_purpose_drilldown cardFeaturesItem'
        except TimeoutException:
            card = self.driver.find_element_by_class_name('miniCard__content')  
            class_ = 'miniCard__descText'
        soup = BeautifulSoup(card.get_attribute('innerHTML'))
        
        try:
            return soup.find(class_=class_).text.split(',')[0]
        except AttributeError:
            return 'unknown'
        
        
    def get_districts(self, list_of_streets, exit=True):
        """Apply get_district on a list of streets."""
        
        districts = []
        for street in list_of_streets:
            #nu pochemu u nih million variantov UI
            try:
                districts.append(self.get_district(street))
            except NoSuchElementException:
                districts.append('unknown')           
        if exit:
            self.exit()
        return districts
    
    def exit(self):
        self.driver.quit()