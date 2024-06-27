import geopandas as gpd
import numpy as np
from shapely.geometry import box
from random import uniform
from collections import Counter

input_file = 'Great-Barrier-Reef-and-Torres-Strait-20230310013521/Geomorphic-Map/geomorphic.gpkg'
geomorphic_zones = gpd.read_file(input_file)

print("Loaded geomorphic zones geometry")

if not geomorphic_zones.crs.is_projected:
    geomorphic_zones = geomorphic_zones.to_crs('EPSG:32619')


minx, miny, maxx, maxy = geomorphic_zones.total_bounds


rectangle_size = 10

def create_random_rectangle(minx, miny, maxx, maxy):
    x = uniform(minx, maxx - rectangle_size)
    y = uniform(miny, maxy - rectangle_size)
    return box(x, y, x + rectangle_size, y + rectangle_size)

from rtree import index

geomorphic_index = index.Index()
for idx, geom in enumerate(geomorphic_zones.geometry):
    geomorphic_index.insert(idx, geom.bounds)

print("Created spatial index")

num_rectangles = 100000
rectangles = []

stats = {}
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
        if classes_tuple not in stats:
            stats[classes_tuple] = 0
        stats[classes_tuple] += 1

        if len(rectangles) % 1000 == 0:
            print(f'Rectangle {len(rectangles)} / {num_rectangles} created in {classes_tuple} after {tries} tries')

        rectangles.append(rectangle)
        tries = 0

    # intersects = geomorphic_zones.intersects(rectangle)
    # if intersects.any():
    #     geomorphic_zone = geomorphic_zones[intersects]
    #     geomorphic_zone_name = geomorphic_zone['class'].values[0]
    #     if geomorphic_zone_name not in stats:
    #         stats[geomorphic_zone_name] = 0
    #     stats[geomorphic_zone_name] += 1

    #     rectangles.append(rectangle)
    #     print(f'Rectangle {len(rectangles)} / {num_rectangles} created in {geomorphic_zone_name}')

# calculate percentage of rectangles in each geomorphic zone
for zone_name, count in stats.items():
    print(f'{zone_name}: {count / num_rectangles * 100:.3f}%')
    stats[zone_name] = count / num_rectangles * 100

# export as json file
import json

with open(input_file.split('/')[0] + '_output.json', 'w') as f:
    json.dump(stats, f, indent=4)



# visualize the rectangles and geomorphic zones
# import matplotlib.pyplot as plt

# fig, ax = plt.subplots(figsize=(10, 10))
# geomorphic_zones.plot(ax=ax, edgecolor='black')
# for rectangle in rectangles:
#     x, y = rectangle.exterior.xy
#     ax.fill(x, y, color='red', alpha=0.5)

# plt.show()




