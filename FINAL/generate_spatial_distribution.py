import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class CoralSpecies:
    def __init__(self, name, radius, clustering_factor, color):
        self.name = name
        self.radius = radius
        self.clustering_factor = clustering_factor
        self.color = color

def generate_position_clustering(colonies, species_name, clustering_factor, parent_radius, max_attempts=100):
    attempts = 0
    same_species_colonies = [colony for colony in colonies if colony['species'] == species_name]
    
    while attempts < max_attempts:
        if same_species_colonies and random.random() < clustering_factor:
            # pick existing colony of the same species 
            base_colony = random.choice(same_species_colonies)
            angle = random.uniform(0, 2 * np.pi)

            min_distance = base_colony['radius'] + parent_radius

            distance = random.uniform(min_distance, min_distance + base_colony['radius'] * 2)
            x = base_colony['x'] + distance * np.cos(angle)
            y = base_colony['y'] + distance * np.sin(angle)
        else:
            # random position if no colonies or if clustering factor is low
            x = random.uniform(0, 10)
            y = random.uniform(0, 10)

        if 0 <= x <= 10 and 0 <= y <= 10:
            return x, y
        attempts += 1

    return random.uniform(0, 10), random.uniform(0, 10)

# check overlap with grid-based approach
def check_overlap(grid, grid_size, x, y, radius):
    grid_x = int(x // grid_size)
    grid_y = int(y // grid_size)
    for i in range(max(0, grid_x-1), min(10, grid_x+2)):
        for j in range(max(0, grid_y-1), min(10, grid_y+2)):
            for colony in grid[(i, j)]:
                dist = np.sqrt((colony['x'] - x) ** 2 + (colony['y'] - y) ** 2)
                if dist < (colony['radius'] + radius):
                    return True
    return False

def place_coral_colonies(species_list, colony_counts, grid_size=1):
    colonies = []
    grid = defaultdict(list) 

    for species, count in zip(species_list, colony_counts):
        for _ in range(count):
            radius = species.radius
            while True:
                x, y = generate_position_clustering(colonies, species.name, species.clustering_factor, radius)
                if x - radius >= 0 and x + radius <= 10 and y - radius >= 0 and y + radius <= 10 and not check_overlap(grid, grid_size, x, y, radius):
                    colony = {'species': species.name, 'x': x, 'y': y, 'radius': radius, 'color': species.color}
                    colonies.append(colony)
                    grid[int(x // grid_size), int(y // grid_size)].append(colony)
                    break
    return colonies

def visualize_terrain(colonies):
    fig, ax = plt.subplots()
    for colony in colonies:
        circle = plt.Circle((colony['x'], colony['y']), colony['radius'], color=colony['color'], alpha=0.5)
        ax.add_artist(circle)
        ax.text(colony['x'], colony['y'], colony['species'][0], fontsize=8, ha='center', va='center')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    plt.show()

species_list = [
    # CoralSpecies("A", 0.2, 1.0, 'blue'),  
    # CoralSpecies("B", 0.3, 0.2, 'green'), 
    # CoralSpecies("C", 0.2, 1.0, 'purple'), 
    # CoralSpecies("D", 0.4, 0.1, 'red') 
]

total_colonies = 1000
colony_counts = []

# read generated_species_abundance.json
import json

with open('generated_species_abundance.json', 'r') as f:
    species_abundance = json.load(f)

    for species in species_abundance:
        print(species)
        species_list.append(CoralSpecies(species, .1, 0.1, 'blue'))
        colony_counts.append(int(species_abundance[species] * total_colonies))

colonies = place_coral_colonies(species_list, colony_counts)
visualize_terrain(colonies)

# export json file of the list of [species, x, y]
output = []
for colony in colonies:
    output.append([colony['species'], colony['x'], colony['y']])

with open('generated_spatial_distribution.json', 'w') as f:
    json.dump(output, f, indent=4)