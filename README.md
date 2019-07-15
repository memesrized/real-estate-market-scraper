# Requirements
 - Firefox v68.0
 - geckodriver v0.24.0
 - libs in requirements.txt
 - python v3.7.3
 
# How to use 
1. Setup requirements described above.
2. Setup config with your Google maps API key. (turn on GeocoderAPI and JavascriptAPI).

    `$ python set_config.py YOUR_KEY`
    
3. Run commands for each city

    `make spb`
    
    `make msk`
    
    `make ekb`
4. Create map images:
    
    `make screenshot_all`
    
    or
    
    you can check `map_notebook.ipynb` and even interact with map.
    


![alt text](https://i.kym-cdn.com/entries/icons/original/000/021/311/free.jpg)
