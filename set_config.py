#!/usr/bin/env python
# coding: utf-8

# In[3]:


import io
import yaml
import sys

# Define data
data = {'API_key':sys.argv[1]}

# Write YAML file
with io.open('config.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

