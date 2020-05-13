# BetaLibrary

Your complement to bouldering guides. Check the beta provided by [MadBoulder](https://www.youtube.com/channel/UCX9ok0rHnvnENLSK7jdnXxA). Powered by [Flask](http://flask.pocoo.org/) and [Folium](https://python-visualization.github.io/folium/), with a little help from [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/#).

You can check it at: [https://madboulder.org](https://madboulder.org)

<p align="center" style="text-align:center;">
<img src="/extras/home.png"><br>
Main Page
</p>

<p align="center" style="text-align:center;">
<img src="/extras/map.png"><br>
Zones Map
</p>

<p align="center" style="text-align:center;">
<img src="/extras/detail.png"><br>
Sector Map
</p>

## About

This project complements [MadBoulder](https://www.youtube.com/channel/UCX9ok0rHnvnENLSK7jdnXxA)'s beta video library and makes it easier to navigate through the available information. It is **NOT** a topo guide of bouldering areas and has no intention of becoming so. It is intended to be used along the bouldering guides of each area and its main goal is to simplify and ease the process of finding beta for specific problems.

If you have any beta recorded feel free to drop it at https://madboulder.org/upload


## Usage

You can visit the page at: [https://madboulder.org](https://madboulder.org)

To build the project locally follow the next steps:

1. Make sure you have Python3, [Flask](http://flask.pocoo.org/), [Folium](https://python-visualization.github.io/folium/), [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/#) and [Flask-Babel](https://pythonhosted.org/Flask-Babel/) installed. [Flask Mail](https://pythonhosted.org/Flask-Mail/) is also used but it is not required. I recomend to install everything in a [virtual environment](https://virtualenv.pypa.io/en/latest/). (After cloning the repository you can install the required packages with: `$ pip install -r /path/to/requirements.txt`) **WARNING: There are several dependencies no longer required that are still present in the requirements file**.
2. Clone the repository by tipying in a terminal `$ git clone https://github.com/MadBoulder/BetaLibrary.git`
3. `cd` to `BetaLibrary` and run `$ python generate_templates.py` and `$ python generate_pages.py`. Additionally, to update the video database with new videos added to the channel, run `$ python get_channel_data.py`.
4. Run `$ python application.py` and visit `http://127.0.0.1:5000/`

## Information for developers and contributors

### Translations

Documentation: [https://pythonhosted.org/Flask-Babel/](https://pythonhosted.org/Flask-Babel/)

#### Add new language

1. Open `config.py` and add the desired language locale to the `LANGUAGES` list.
2. Create the language catalog: `$ pybabel init -i messages.pot -d translations -l [LOCALE]`, where `[LOCALE]` should be replaced by the new locale.

#### Extracting/Updating translations

To extract all the texts that are to be translated to the `.pot` file use the following command:
`$ pybabel extract -F babel.cfg -k _l -o messages.pot .`

To update all catalogs with the latest set of messages:
`$ pybabel update -i messages.pot -d translations`

#### Compile translations

After all translations have been added or updated in the respective `.po` files (found under `translations/[LOCALE]/LC_MESSAGES/messages.po`), to make the changes effective the translations have to be recompiled. This is achieved with the following command: `$ pybabel compile -d translations`

### Zones and Sectors

The sections below outline how new zone and sector data should be added to the project.

### Folder Structure

To create a new zone and its sectors:
1. Create a new folder inside `data/zones` with the name of the zone (`data/zones/NEW_ZONE_NAME`).
2. Inside this new folder `data/zones/NEW_ZONE_NAME` create a `NEW_ZONE_NAME.txt`.
3. If the zone has sectors (which is not mandatory), create a new folder inside `data/zones/NEW_ZONE_NAME` and name it `sectors` (`data/zones/NEW_ZONE_NAME/sectors`).
4. For each sector, create a `SECTOR_NAME.txt` inside the `sectors` folder.

So far the zone structure should be:

```bash
data/zones
       |
       --- NEW_ZONE_NAME
                |
                --- NEW_ZONE_NAME.txt
                |
                --- sectors
                      |
                      --- SECTOR_NAME_1.txt
                      |
                      --- SECTOR_NAME_2.txt
```

### Zone and Sector Data