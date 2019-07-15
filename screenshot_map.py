#!/usr/bin/env python
# coding: utf-8

# In[3]:


import sys
import time
import selenium.webdriver

reg = sys.argv[1]
res1 = sys.argv[2]
res2 = sys.argv[3]

driver = selenium.webdriver.Firefox()
driver.set_window_size(res1, res2)  # choose a resolution
driver.get(f'http://localhost:1337/{reg}.html')
# You may need to add time.sleep(seconds) here

time.sleep(5)

driver.save_screenshot(f'./cities/screenshot_{reg}.png')

