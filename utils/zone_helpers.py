import json
from werkzeug.utils import secure_filename
import handle_channel_data


def get_problems_from_zone(zone_code):
    """
    Given a zone name, return all problems we have for that area
    Cache for 24 hours or something like that? - We might have to
    adjust how this gets computed.

    We can build the list from the processed data file, which will
    speed things up and avoid using 3rd party service quotas. Problem
    is that the list has to be kept up to date.

    The second dilemma is about generating the file dinamically or 
    statically. When it comes to indexation I guess it is better to
    have the pages statically created?
    """
    with open('data/channel/processed_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # process data
    with open(f'data/zones/{zone_code}/{zone_code}.json', 'r', encoding='utf-8') as z:
        zone_name = json.load(z)['name']
    # filter data by zone and extract problem name
    problems = [p for p in data['items'] if p['zone'] == zone_name]
    for p in problems:
        p['name'] = get_problem_name(p)
    return problems


def get_problem_name(problem_data):
    """
    Ugly function to remove pieces from the video 
    title until we are left with the problem name
    """
    # remove grade from title?
    name = problem_data['name']
    if name == 'Unknown':
        print(problem_data['title'])
        name = problem_data['title'].replace(
            problem_data.get('zone', ''), ''
        ).replace(
            problem_data.get('grade', '').lower(), ''
        ).replace(
            problem_data.get('grade', '').upper(), ''
        ).replace(
            '(sit)',
            ''
        ).replace(
            '(stand)',
            ''
        ).replace(
            '(crouching start)',
            ''
        ).strip()

        if name[-1] == '.':
            name = name[:-1].strip()
        if name[-1] == ',':
            name = name[:-1].strip()
    print(name)
    return name
    
    
def get_problems_from_sector(problems_zone, sector_code):
    problems = []
    for p in problems_zone:
        if secure_filename(p['sector']) == sector_code:
            problems.append(p)

    return problems
    
    
def get_sectors_from_zone(zone_code):
    problems = get_problems_from_zone(zone_code)
    sectors = []
    for p in problems:
        alreadyAdded=False
        for s in sectors:
            if s[0] == p['sector']:
                alreadyAdded=True
                break
        if not alreadyAdded:
            sectors.append([p['sector'], secure_filename(p['sector'])])
            
    if len(sectors) == 1:
        if sectors[0] == "Unknown":
            return None
    return sectors
    
   
def get_playlist_url_from_sector(zone_code, sector):
    print("get_playlist_url_from_sector zone_code:" + zone_code + " sector: " + sector)
    playlists = get_playlists_url_from_zone(zone_code)
    if 'sectors' in playlists:
        for playlist in playlists['sectors']:
            if secure_filename(playlist['name']) == sector:
                return playlist['url']
    return None
    
    
def get_playlists_url_from_zone(zone_code):
    print("get playlists of " + zone_code)
    zone_data = handle_channel_data.get_zone_data()

    playlists = []
    for item in zone_data['items']:
        if item['zone_code'] == zone_code:
            playlists = item
            break
            
    return playlists
    

def load_data(infile):
    """
    Load current data stored in the project folder
    """
    video_data = []
    if infile:
        with open(infile, 'r', encoding='utf-8') as f:
            try:
                video_data = json.load(f)['items']
            except:
                pass
    return video_data


if __name__ == "__main__":
    get_playlists_url_from_zone("Albarracín")