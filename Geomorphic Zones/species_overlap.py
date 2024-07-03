import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import box, Point
from random import uniform
from collections import Counter

data = pd.read_csv('species/combined_occurences.csv', sep='\t')
# filter rows that have NaN values in 'decimalLatitude' and 'decimalLongitude'
data = data.dropna(subset=['decimalLatitude', 'decimalLongitude'])

species_gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.decimalLongitude, data.decimalLatitude))
species_gdf.crs = 'EPSG:4326'

num_species = len(data)

print(f"{num_species} species loaded")

input_file = 'zones/Hawaiian-Islands-20230309235255/Geomorphic-Map/geomorphic.gpkg'
geomorphic_zones = gpd.read_file(input_file)

def determine_utm_zone(lon, lat):
    utm_zone = int((lon + 180) / 6) + 1
    if lat >= 0:
        epsg_code = 32600 + utm_zone
    else:
        epsg_code = 32700 + utm_zone
    return epsg_code

minx, miny, maxx, maxy = geomorphic_zones.total_bounds
central_longitude = (minx + maxx) / 2
central_latitude = (miny + maxy) / 2

epsg_code = determine_utm_zone(central_longitude, central_latitude)

geomorphic_zones = geomorphic_zones.to_crs(f'EPSG:{epsg_code}')
species_gdf = species_gdf.to_crs(f'EPSG:{epsg_code}')

print(epsg_code, " is the UTM zone for the geomorphic zones and species data")

minx, miny, maxx, maxy = geomorphic_zones.total_bounds

# if geomorphic_zones.crs.is_projected:
#     geomorphic_zones = geomorphic_zones.to_crs('EPSG:4326')

print("Loaded geomorphic zones geometry")


minx, miny, maxx, maxy = geomorphic_zones.total_bounds

from rtree import index

geomorphic_index = index.Index()
for idx, geom in enumerate(geomorphic_zones.geometry):
    geomorphic_index.insert(idx, geom.bounds)

print("Created spatial index")

stats = {}
stats_certain10 = {}
stats_certain100 = {}

for index, species in species_gdf.iterrows():
    
    x, y = species.geometry.x, species.geometry.y

    point = Point(x, y)
    if x < minx or x > maxx or y < miny or y > maxy:
        continue

    rectangle = box(x, y, x + 0.1, y + 0.1)

    possible_matches_index = list(geomorphic_index.intersection(point.bounds))
    possible_matches = geomorphic_zones.iloc[possible_matches_index]
    overlapping_zones = possible_matches[possible_matches.intersects(point)]

    if len(overlapping_zones) > 0:
        classes = overlapping_zones['class'].unique()
        classes_tuple = " & ".join(sorted(classes))

        if index % 100 == 0:
            print(species['species'], classes_tuple, " ", index + 1, " / ", num_species)

        if classes_tuple not in stats:
            stats[classes_tuple] = {}
        if species['coordinateUncertaintyInMeters'] <= 100 and classes_tuple not in stats_certain100:
            stats_certain100[classes_tuple] = {}
        if species['coordinateUncertaintyInMeters'] <= 10 and classes_tuple not in stats_certain10:
            stats_certain10[classes_tuple] = {}

        if species['species'] not in stats[classes_tuple]:
            stats[classes_tuple][species['species']] = 0
        if species['coordinateUncertaintyInMeters'] <= 100 and species['species'] not in stats_certain100[classes_tuple]:
            stats_certain100[classes_tuple][species['species']] = 0
        if species['coordinateUncertaintyInMeters'] <= 10 and species['species'] not in stats_certain10[classes_tuple]:
            stats_certain10[classes_tuple][species['species']] = 0

        stats[classes_tuple][species['species']] += 1
        if species['coordinateUncertaintyInMeters'] <= 100:
            stats_certain100[classes_tuple][species['species']] += 1
        if species['coordinateUncertaintyInMeters'] <= 10:
            stats_certain10[classes_tuple][species['species']] += 1

# calculate percentage of rectangles in each geomorphic zone
# for zone_name, count in stats.items():
#     print(f'{zone_name}: {count:.3f}%')
#     stats[zone_name] = count

# export as json file
import json

with open('results/' + input_file.split('/')[1] + '_species_uncertain.json', 'w') as f:
    json.dump(stats, f, indent=4)

with open('results/' + input_file.split('/')[1] + '_species_certain100.json', 'w') as f:
    json.dump(stats_certain100, f, indent=4)

with open('results/' + input_file.split('/')[1] + '_species_certain10.json', 'w') as f:
    json.dump(stats_certain10, f, indent=4)




rectangle_size = 10

def create_random_rectangle(minx, miny, maxx, maxy):
    x = uniform(minx, maxx - rectangle_size)
    y = uniform(miny, maxy - rectangle_size)
    return box(x, y, x + rectangle_size, y + rectangle_size)

num_rectangles = 100000
rectangles = []

rectangle_stats = {}
tries = 0

total_area = sum(zone.area for zone in geomorphic_zones.geometry)
zone_weights = [zone.area / total_area for zone in geomorphic_zones.geometry]
zone_weights = np.array(zone_weights)

print("The total area of the geomorphic zones is", total_area)

while len(rectangles) < num_rectangles:
    tries += 1

    # Sample a zone with probability proportional to its area
    zone_idx = np.random.choice(geomorphic_zones.index, p=zone_weights)
    zone_geometry = geomorphic_zones.geometry.iloc[zone_idx]

    rectangle = create_random_rectangle(*zone_geometry.bounds)

    possible_matches_index = list(geomorphic_index.intersection(rectangle.bounds))
    possible_matches = geomorphic_zones.iloc[possible_matches_index]
    overlapping_zones = possible_matches[possible_matches.intersects(rectangle)]

    if len(overlapping_zones) > 0:
        classes = overlapping_zones['class'].unique()
        classes_tuple = " & ".join(sorted(classes))
        if classes_tuple not in rectangle_stats:
            rectangle_stats[classes_tuple] = 0
        rectangle_stats[classes_tuple] += 1

        if len(rectangles) % 1000 == 0:
            print(f'Rectangle {len(rectangles)} / {num_rectangles} created in {classes_tuple} after {tries} tries')

        rectangles.append(rectangle)
        tries = 0

with open('results/' + input_file.split('/')[1] + '_zones.json', 'w') as f:
    json.dump(rectangle_stats, f, indent=4)



# # visualize the rectangles and geomorphic zones
# # import matplotlib.pyplot as plt

# # fig, ax = plt.subplots(figsize=(10, 10))
# # geomorphic_zones.plot(ax=ax, edgecolor='black')
# # for rectangle in rectangles:
# #     x, y = rectangle.exterior.xy
# #     ax.fill(x, y, color='red', alpha=0.5)

# # plt.show()




