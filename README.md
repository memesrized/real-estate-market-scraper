# Requirements
 - Firefox v68.0
 - geckodriver v0.24.0
 - libs in requirements.txt
 - python v3.7.3
 
# How to use 
1. Setup requirements described above.
2. Setup config with your Google maps API key (turn on GeocoderAPI and JavascriptAPI).

    `$ python set_config.py YOUR_KEY`
    
    Contact me if you need my key.
    
3. Run commands for each city

    `make spb`
    
    `make msk`
    
    `make ekb`
4. Create map images:
    
    `make screenshot_all`
    
    or
    
    you can check `map_notebook.ipynb` and even interact with map
    
    or 
    
    `python3.7 -m http.server 2019` and open `http://localhost:2019/YOUR_MAP.html` and screenshot any way you want.
    
# Repo
cities/ - raw datasets and output images

datasets/ - corrected datasets

spb|msk|ekb/ - set of datasets on each parsed page 

# Note
There is no hist by default for Moscow because 2GIS doesnt contain districts (муниципальные округа) for msk. You can still create hist, but it will be grouped by street name.

![alt text](https://i.kym-cdn.com/entries/icons/original/000/021/311/free.jpg)
