import folium
import pandas
import os
from dotenv import load_dotenv

def color_range(elevation):
    if elevation < 1000:
        return 'green'
    elif elevation < 3000:
        return 'orange'
    else:
        return 'red'

def create_map():
    load_dotenv()
    mapbox_access_token = os.getenv('MAPBOX_ACCESS_TOKEN')

    base_path = os.path.dirname(os.path.abspath(__file__))
    volcanoes_path = os.path.join(base_path, '..', 'data', 'Volcanoes.txt')
    world_json_path = os.path.join(base_path, '..', 'data', 'world.json')

    data = pandas.read_csv(volcanoes_path)
    latitude = list(data['LAT'])
    longitude = list(data['LON'])
    elevation = list(data['ELEV'])

    map = folium.Map(
        location=[47.03, 8.09],
        zoom_start=6,
        tiles=f'https://api.mapbox.com/styles/v1/mapbox/bright-v9/tiles/{{z}}/{{x}}/{{y}}?access_token={mapbox_access_token}',
        attr='Mapbox'
    )

    fgv = folium.FeatureGroup(name="Volcanoes")

    for lat, lon, elev in zip(latitude, longitude, elevation):
        fgv.add_child(folium.Marker(
            location=[lat, lon],
            popup=str(elev) +" M",
            icon=folium.Icon(color=color_range(elev))
        ))

    fgp = folium.FeatureGroup(name="Population")

    def style_function(feature):
        pop = feature['properties']['POP2005']
        return {
            'fillColor': 'green' if pop < 10000000 else
                         'yellow' if 10000000 <= pop < 40000000 else
                        'orange' if 40000000 <= pop < 80000000 else
                         'red',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.5
        }

    with open(world_json_path, 'r', encoding='utf-8-sig') as f:
        geojson_data = f.read()

    fgp.add_child(folium.GeoJson(
        data=geojson_data,
     style_function=style_function
    ))

    map.add_child(fgv)
    map.add_child(fgp)
    map.add_child(folium.LayerControl())

    map.save('Map1.html')
