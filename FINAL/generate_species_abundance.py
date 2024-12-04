import os
import pandas as pd
import random
import json
import argparse

# Read the geomorphic stats from folder statistics
def read_geomorphic_stats(base_folder):
    geomorphic_data = {}

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

def read_geomorphic_zones_overlap(json_file_path):
    with open(json_file_path, 'r') as f:
        geomorphic_zones_overlap = json.load(f)
    return geomorphic_zones_overlap

def weighted_choice(choices, weights):
    total_weight = sum(weights)
    normalized_weights = [w / total_weight for w in weights]
    return random.choices(choices, weights=normalized_weights, k=1)[0]

def calculate_species_abundance(geomorphic_zone_folder='geomorphic_zones', geomorphic_zones_overlap_path='analysis_results/geomorphic_zones_overlap.json'):
    geomorphic_data = read_geomorphic_stats(geomorphic_zone_folder)
    geomorphic_zones_overlap = read_geomorphic_zones_overlap(geomorphic_zones_overlap_path)

    # Step 1: Weighted random selection of the mapped area based on 'cover_sqkm'
    total_area = sum(x['cover_sqkm'] for x in geomorphic_data.values())
    mapped_areas = list(geomorphic_data.keys())
    mapped_area_weights = [geomorphic_data[mapped_area]['cover_sqkm'] / total_area for mapped_area in mapped_areas]

    chosen_mapped_area = random.choices(mapped_areas, weights=mapped_area_weights, k=1)[0]
    
    print(f"Chosen mapped area: {chosen_mapped_area}")
    
    # Step 2: Weighted random selection of the geomorphic zone from the chosen mapped area
    if chosen_mapped_area in geomorphic_zones_overlap:
        zone_data = geomorphic_zones_overlap[chosen_mapped_area]
        # for now: exclude zone combinations
        zone_data = {k: v for k, v in zone_data.items() if '&' not in k}

        zones = list(zone_data.keys())
        zone_weights = list(zone_data.values())
        
        chosen_zone = weighted_choice(zones, zone_weights)
        
        print(f"Chosen zone: {chosen_zone}")
    else:
        print(f"No zone data available for the mapped area: {chosen_mapped_area}")
        return

    # Step 3: Load species data for the chosen zone
    with open('analysis_results/species_analysis_results.json', 'r') as f:
        species_data = json.load(f)

        if chosen_mapped_area in species_data and chosen_zone in species_data[chosen_mapped_area]:
            species_abundance = species_data[chosen_mapped_area][chosen_zone]
        else:
            print(f"No species data available for {chosen_zone} in {chosen_mapped_area}")
            return
        
        # Normalize species abundance values
        total_occ = sum(species_abundance.values())
        if total_occ > 0:
            for species in species_abundance:
                species_abundance[species] /= total_occ

        with open('species_abundance.json', 'w') as f:
            json.dump(species_abundance, f, indent=4)
        
        return species_abundance

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "geomorphic_zone_folder",
        nargs="?",
        default="geomorphic_zones"
    )
    parser.add_argument(
        "geomorphic_zones_overlap_path",
        nargs="?",
        default="analysis_results/geomorphic_zones_overlap.json"
    )

    args = parser.parse_args()
    calculate_species_abundance(args.geomorphic_zone_folder, args.geomorphic_zones_overlap_path)

if __name__ == "__main__":
    main()