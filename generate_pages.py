import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json


def main():
    """
    Generate html map templates for all the areas located inside the data folder
    as well as a general map that contains all the areas
    """
    areas = next(os.walk('data/'))[1]
    all_data = ['data/' + area + '/' + area + '.txt' for area in areas]

    template_loader = FileSystemLoader( searchpath="." )
    template_env = Environment( loader=template_loader )

    for area in areas:
        print(area)
        datafile = 'data/' + area + '/' + area + '.txt'
        area_data = {}
        with open(datafile) as data:
            area_data = json.load(data)

        template = template_env.get_template('templates/zone_layout.html')
        output = template.render(name=area_data['name'], guide_list=area_data['guides'], map_url='maps/'+area)
        with open('templates/zones/'+area+'.html', 'w') as template:
            template.write(output)


if __name__ == '__main__':
    main()
