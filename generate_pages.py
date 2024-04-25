import os
from jinja2 import Environment, FileSystemLoader
import json
import utils.helpers
import utils.zone_helpers
import utils.MadBoulderDatabase
from slugify import slugify

LINK_FIELD = 'link'
NAME_FIELD = 'name'
ZONE_CODE_FIELD = 'zone_code'
LATITUDE_FIELD = 'latitude'
LONGITUDE_FIELD = 'longitude'
ALTITUDE_FIELD = 'altitude'
GUIDES_FIELD = 'guides'
SECTORS_FIELD = 'sectors'
LINKS_FIELD = 'links'
COUNTRY_CODE_FIELD = 'country'
STATE_CODE_FIELD = 'state'
ROCK_TYPE_FIELD = 'rock_type'
OVERVIEW_FIELD = 'overview'


def main():
    """
    Generate html map templates for all the areas located inside the data folder
    as well as a general map that contains all the areas
    """
    areas = utils.MadBoulderDatabase.getAreasData()
    playlists = utils.MadBoulderDatabase.getPlaylistsData()

    template_loader = FileSystemLoader(searchpath='.')
    template_env = Environment(loader=template_loader)

    generateAreasListPage(template_env, areas, playlists)

    templatePage = template_env.get_template('templates/templates/area_page_template.html')
    templatePage_es = template_env.get_template('templates/templates/es/area_page_template.html')

    playlists = {}
    total_areas = len(areas)
    for areaCode, area in areas.items():
        print(f"Creating area page of {area[NAME_FIELD]}")
        
        # get external links
        links = [link for link in area.get(LINKS_FIELD, []) if link.get(LINK_FIELD)]
        # get external guides
        guides = [
            {
                "name": guide["name"],
                "link": guide["link"][0] if isinstance(guide["link"], list) else guide["link"],
                "thumbnail": guide["thumbnail"]
            }
            for guide in area.get(GUIDES_FIELD, [])
            if guide.get(LINK_FIELD)
        ]
        guides = [guide for guide in guides if guide.get(LINK_FIELD)]

        # problems
        problems = utils.MadBoulderDatabase.getVideoDataFromZone(areaCode)
        problems.sort(key= lambda x: x['name'])
            
        # sectors
        sectors = utils.zone_helpers.get_sectors_from_zone(areaCode)
        sectors.sort(key= lambda x: x)
        
        #playlists
        playlists = utils.zone_helpers.get_playlists_from_zone(areaCode)

        #country
        areaInfo = utils.zone_helpers.getStateAndCountryInfo(areaCode)

        #overview
        overview = area.get("overview", [""])[0]
        
        output = templatePage.render(
            problems=problems,
            sectors=sectors,
            area_code=areaCode,
            name=area[NAME_FIELD],
            rock_type=utils.zone_helpers.get_rock_type_str(area.get(ROCK_TYPE_FIELD, "")),
            overview=overview,
            tag_name=area[NAME_FIELD].replace("'", r"\'"),
            links_list=links,
            guides_list=guides,
            map_url='maps/'+areaCode,
            playlists=playlists,
            lat=area[LATITUDE_FIELD],
            lng=area[LONGITUDE_FIELD],
            alt=int(area.get(ALTITUDE_FIELD,'0')),
            zone=area[NAME_FIELD],
            areaInfo=areaInfo
        )

        with open('templates/zones/'+areaCode+'.html', 'w', encoding='utf-8') as template:
            template.write(output)

        guides_es = [
            {
                "name": guide["name"],
                "link": guide["link"][1] if isinstance(guide["link"], list) else guide["link"],
                "thumbnail": guide["thumbnail"]
            }
            for guide in area.get(GUIDES_FIELD, [])
            if guide.get(LINK_FIELD)
        ]
        guides_es = [guide for guide in guides_es if guide.get(LINK_FIELD)]
        overview_es = area.get("overview", [""])[1]

        output = templatePage_es.render(
            problems=problems,
            sectors=sectors,
            area_code=areaCode,
            name=area[NAME_FIELD],
            rock_type=utils.zone_helpers.get_rock_type_str(area.get(ROCK_TYPE_FIELD, "")),
            overview=overview_es,
            tag_name=area[NAME_FIELD].replace("'", r"\'"),
            links_list=links,
            guides_list=guides_es,
            map_url='maps/'+areaCode,
            playlists=playlists,
            lat=area[LATITUDE_FIELD],
            lng=area[LONGITUDE_FIELD],
            alt=int(area.get(ALTITUDE_FIELD,'0')),
            zone=area[NAME_FIELD],
            areaInfo=areaInfo
        )

        with open('templates/zones/es/'+areaCode+'.html', 'w', encoding='utf-8') as template_es:
            template_es.write(output)


def generateAreasListPage(template_env, areas, playlists):
    country_data = utils.MadBoulderDatabase.getCountriesData()
    templatePageList = template_env.get_template('templates/templates/areas_list_page_template.html')

    output = templatePageList.render(
        zones=areas,
        playlists=playlists,
        country_data=country_data

    )
    with open('templates/bouldering-areas-list.html', 'w', encoding='utf-8') as template:
        template.write(output)



if __name__ == '__main__':
    main()
