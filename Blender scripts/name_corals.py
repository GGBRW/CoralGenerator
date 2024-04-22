# When the corals are loaded in a Blender scene, they are named after their .obj filename. 
# This script renames the corals to their actual name according to the CORALCATALOG.json file

import bpy
import json

json_file_path = '/Users/ggbrw/Documents/GEO Thesis/CoralGeneratorRepo/Smithsonian Corals scripts/CORALCATALOG.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)

name_mapping = {item['filename'].replace('.obj', ''): item['name'] for item in data}

for obj in bpy.data.objects:
    if obj.name in name_mapping:
        obj.name = name_mapping[obj.name]

print("Renaming complete.")