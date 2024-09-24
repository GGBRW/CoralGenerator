import os
import pandas as pd
import random

def read_geomorphic_stats(base_folder):
    geomorphic_data = {}

    # Loop through all folders in the geomorphic_zones folder
    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)
        
        if os.path.isdir(folder_path):
            stats_folder = os.path.join(folder_path, 'stats')
            csv_file_path = os.path.join(stats_folder, 'statistics.csv')

            if os.path.exists(stats_folder) and os.path.isfile(csv_file_path):
                df = pd.read_csv(csv_file_path)
                
                geomorphic_records = df[df['class_type'] == 'geomorphic']

                if not geomorphic_records.empty:
                    geomorphic_data[folder_name] = {
                        'cover_sqkm': 0,
                        'geomorphic_zones': {}
                    }
                    for index, row in geomorphic_records.iterrows():
                        geomorphic_data[folder_name]['geomorphic_zones'][row['class_name']] = row['cover_fraction']
                        geomorphic_data[folder_name]['cover_sqkm'] += row['cover_sqkm']
                    
    return geomorphic_data

geomorphic_zone_folder = 'geomorphic_zones' 
geomorphic_data = read_geomorphic_stats(geomorphic_zone_folder)

print(geomorphic_data)

def weighted_choice(choices, weights):
    return random.choices(choices, weights=weights, k=1)[0]


# perform weighted choice on mapped area and geomorphic zone
total_area = sum(x['cover_sqkm'] for x in geomorphic_data.values())

mapped_areas = list(geomorphic_data.keys())
mapped_area_weights = [geomorphic_data[mapped_area]['cover_sqkm'] / total_area for mapped_area in mapped_areas]

chosen_mapped_area = weighted_choice(mapped_areas, mapped_area_weights)

chosen_mapped_area_zones = geomorphic_data[chosen_mapped_area]['geomorphic_zones']
zones = list(chosen_mapped_area_zones.keys())
zone_weights = list(chosen_mapped_area_zones.values())

chosen_zone = weighted_choice(zones, zone_weights)

print(f"Chosen mapped_area: {chosen_mapped_area}")
print(f"Chosen zone: {chosen_zone}")



import json

with open('species_analysis_results.json', 'r') as f:
    species_data = json.load(f)

    # pick the chosen mapped_area and zone
    species_abundance = species_data[chosen_mapped_area][chosen_zone]
    print(species_abundance)

    # export as generated_species_abundance.json
    with open('generated_species_abundance.json', 'w') as f:
        json.dump(species_abundance, f, indent=4)

