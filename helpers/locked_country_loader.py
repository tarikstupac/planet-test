import json
from redis_conf import country_watcher as r

LOCKED_COUNTRIES = ['Andorra', 'Albania', 'Australia']

def add_locked_countries():

    #read in all the data from geojson file
    with open('countries.geojson') as f:
        data = json.load(f)

    #iterate through countries GEOJSON and add coordinates of countries specified in
    #LOCKED_COUNTRIES constant to the redis tile38 instance.
    for feature in data['features']:
        if feature['properties']['ADMIN'] in LOCKED_COUNTRIES:
            r.execute_command('SET', 'countries', f'{feature["properties"]["ADMIN"]}', 'OBJECT', json.dumps(feature['geometry']))


if __name__ == '__main__':
    add_locked_countries()


