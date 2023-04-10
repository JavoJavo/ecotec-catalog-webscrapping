[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://javojavo-stoves-catalog-webs-streamlit-appvisualizations-dym14c.streamlit.app/)                     
# stoves-catalog-webscrapping
Webscrapping stove information from https://cleancooking.org/ with selenium (python).


## Resources
- OS: Windows 11
- web page: http://catalog.cleancookstoves.org/
- python
- selenium ([documentation](https://selenium-python.readthedocs.io/index.html))
- Web browser: Google Chrome (https://www.google.com/chrome/) 
- Chrome webdriver: https://chromedriver.chromium.org/downloads (it has to be the same version of your regular Google Chrome web browser)
- Streamlit and plotly for visualization


## Steps
1. Download the file `capture_catalog.py`.
1. Check your google chrome version.
2. Download [chrome webdriver](https://www.google.com/chrome/) with the same version as your google chrome version, preferably store it in the same directory as `capture_catalog.py`. Unzip it.
3. If you saved the chrome webdriver in another directory add its path at line 70 of the `capture_catalog.py` file, where the variable driver is initialized.
4. Run `capture_catalog.py` and zoom out to the max when the new window pops up (depending on the size of your screen, some elements may not be available to click on if the zoom is in its default value).


## Results
- Some stoves contained double quotes, so that messed the resulting csv. At the moment that was handled manually and one instance was deleted completely because it couldn't be made sense of. 


## Visualizations
https://javojavo-stoves-catalog-webs-streamlit-appvisualizations-dym14c.streamlit.app/               
### DEMO visualizations
![demo1](https://github.com/JavoJavo/stoves-catalog-webscrapping/blob/main/peso_neto-flujo_luminoso-vida_util-potencia.png)
![demo2](https://github.com/JavoJavo/stoves-catalog-webscrapping/blob/main/pot_cap-stove_feed_max-stove_price_average-stove_flife-Fit_line.png)

## TODO
1. Handle the double quotes so it doesn't mess the resulting csv file.
2. Check empty fields and add an error label to the csv.
3. Fix bugs that prevent existing fields from being captured if they exist.
4. Search for unadded fields that could be present later on on the stoves, but because they were not present on the first stoves (where the program was based on) they were omitted.
5. Develop visualizations, maybe use streamlit.
6. Remove repeated columns. Check out why they are repeated and make sure no data is lost.
7. Add demo visualizations here on the README.
