import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


def main():
    """
    Generate html map templates for all the areas located inside the data folder
    as well as a general map that contains all the areas
    """
    areas = next(os.walk('data/zones/'))[1]
    all_data = ['data/zones/' + area + '/' + area + '.txt' for area in areas]

    template_loader = FileSystemLoader( searchpath="." )
    template_env = Environment( loader=template_loader )

    playlists = {}
    for area in areas:
        # Create zone map
        print(area)
        datafile = 'data/zones/' + area + '/' + area + '.txt'
        area_data = {}
        with open(datafile) as data:
            area_data = json.load(data)

        playlists[area] = area_data['playlist']
        guides = [(guide['name'], guide['link']) for guide in area_data['guides']]

        template = template_env.get_template('templates/zone_layout.html')
        output = template.render(name=area_data['name'], guide_list=guides, map_url='maps/'+area)
        with open('templates/zones/'+area+'.html', 'w') as template:
            template.write(output)

    # Update playlists file
    with open('data/playlist.txt', 'w') as playlists_file:
        playlists_file.write(json.dumps(playlists))

if __name__ == '__main__':
    main()
