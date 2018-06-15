import folium
import pandas as pd

def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif elevation < 3000:
        return "orange"
    else:
        return "red"

data = pd.read_csv("Volcanoes_USA.txt")

lat = data["LAT"]
lon = data["LON"]
elev = data["ELEV"]

map = folium.Map(location = [38.58, -99.09], zoom_start = 6, tiles = "Mapbox Bright")

fgv = folium.FeatureGroup(name = "Volcanoes")
fgc = folium.FeatureGroup(name = "Population coloring")

for la, lo, el in zip(lat, lon, elev):
    fgv.add_child(
        folium.CircleMarker(location = (la, lo),
                        popup = str(el),
                        color = "grey",
                        radius = 6,
                        fill = True,
                        fill_color = color_producer(el),
                        fill_opacity = .8))

fgc.add_child(
    folium.GeoJson(
        data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
        style_function = lambda x: {'fillColor' : 'green' if x['properties']['POP2005'] < 10000000
                                    else 'orange' if 10000000 <= x['properties']['POP2005'] < 25000000 else 'red'}
        ))

map.add_child(fgv)
map.add_child(fgc)
map.add_child(folium.LayerControl())

map.save("Map1.html")
