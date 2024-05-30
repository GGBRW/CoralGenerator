import json
from check_CFD_ready import check_mesh

json_file_path = '/Users/ggbrw/Documents/GEO Thesis/CoralGeneratorRepo/Smithsonian Corals scripts/CORALCATALOG.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)

file_path = 'Smithsonian Corals scripts/filtered_corals/' + data[22]['filepath'].replace(".obj", "_adj.obj")
print("Checking mesh at", file_path)
check_mesh(file_path)