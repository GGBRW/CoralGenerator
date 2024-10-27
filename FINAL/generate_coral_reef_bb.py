import bpy
import bmesh
import math
import mathutils
from mathutils import noise, Vector, Matrix
import json
import random
import numpy as np
import os
import sys

# Always the first thing to do when working with Blender, remove the 'default cube' :)
bpy.ops.wm.read_factory_settings(use_empty=True)

# PARAMETERS FOR TERRAIN GENERATION (fBm)
overall_slope = math.radians(10)      # Overall slope of the terrain (in radians)
overall_aspect = math.radians(45)  # Overall aspect of the terrain (in radians)
depth = 5.0              # (Water) depth of the terrains center

terrain_size = 100  # Number of grid points (both x and y)
grid_extent = 10.0  # Total size of the grid in meters (10x10 meters)
grid_spacing = grid_extent / (terrain_size - 1)  # Spacing between points
octaves = 6         # The number of layers of noise (controls fractal detail)
persistence = 0.5   # Controls the amplitude of each octave
lacunarity = 2.0    # Controls the frequency of each octave
scale = 50.0        # Scaling factor for the noise (can adjust based on preference)
height_amplification = 1.0  # Amplify the height variation if necessary

total_abundance = 500
calculate_spatial_distribution = True
species_abundance_file = "species_abundance.json"
# if calculate_spatial_distribution is False:
spatial_distribution_file = "spatial_distribution.json"

# Load species abundance from JSON file
with open(species_abundance_file, "r") as f:
    species_abundance = json.load(f)

# Normalize and calculate actual counts for each species
for coral_name, proportion in species_abundance.items():
    species_abundance[coral_name] = round(proportion * total_abundance)

# Import spatial distribution generation script
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir)
import generate_spatial_distribution

# Load the Smithsonian Institution's 3D models collection JSON file 
with open("SI_catalog.json", "r") as f:
    coral_catalog = json.load(f)

coral_models = {}
for item in coral_catalog:
    coral_name = item["name"]
    if coral_name not in coral_models:
        coral_models[coral_name] = []
    coral_models[coral_name].append(item["filepath"])

# fBm: Generate the terrain

slope_dx = math.sin(overall_aspect) * overall_slope
slope_dy = math.cos(overall_aspect) * overall_slope
terrain_normal = mathutils.Vector((-slope_dx, -slope_dy, 1)).normalized()

def fbm(x, y, octaves, persistence, lacunarity):
    total = 0.0
    frequency = 1.0
    amplitude = 1.0
    max_value = 0.0  # to normalize the result

    for _ in range(octaves):
        total += noise.noise(mathutils.Vector((x * frequency, y * frequency, 0.0))) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= lacunarity
    
    return total / max_value

terrain_mesh = bpy.data.meshes.new("Terrain")
terrain_obj = bpy.data.objects.new("Terrain", terrain_mesh)
bpy.context.collection.objects.link(terrain_obj)

# Create bmesh to store the vertices and faces of the terrain
bm = bmesh.new()

# Store terrain heights in 2D list for sampling
terrain_heights = []

for i in range(terrain_size):
    row_heights = []
    for j in range(terrain_size):
        x = i * grid_spacing
        y = j * grid_spacing

        # Projected noise sampling along terrain's normal
        projected_x = i / scale
        projected_y = j / scale
        z_offset = fbm(projected_x, projected_y, octaves, persistence, lacunarity) * height_amplification

        # Base height from slope at (i, j) and add noise along the normal
        center_x = (terrain_size / 2) * grid_spacing
        center_y = (terrain_size / 2) * grid_spacing
        z_base = -depth + (slope_dx * (x - center_x) + slope_dy * (y - center_y))
        z = z_base + z_offset * terrain_normal.z

        bm.verts.new((x, y, z))
        row_heights.append(z)
    terrain_heights.append(row_heights)

bm.verts.ensure_lookup_table()

# faces of the terrain
for i in range(terrain_size - 1):
    for j in range(terrain_size - 1):
        v1 = bm.verts[i * terrain_size + j]
        v2 = bm.verts[(i + 1) * terrain_size + j]
        v3 = bm.verts[(i + 1) * terrain_size + (j + 1)]
        v4 = bm.verts[i * terrain_size + (j + 1)]

        # two triangular faces for each grid square
        bm.faces.new([v1, v2, v3])
        bm.faces.new([v1, v3, v4])

# write bmesh into the terrain mesh object
bm.to_mesh(terrain_mesh)
bm.free()

# OPTIONAL (for visual purposes): Enable smooth shading for the terrain
terrain_obj.select_set(True)
bpy.ops.object.shade_smooth()

# function to get the closest terrain height
def get_terrain_height(x_pos, y_pos):
    grid_x = int(x_pos / grid_spacing)
    grid_y = int(y_pos / grid_spacing)
    
    if 0 <= grid_x < terrain_size and 0 <= grid_y < terrain_size:
        return terrain_heights[grid_x][grid_y]
    return 0.0 

# Load needed coral models 
loaded_coral_objects = {}

def get_model_radius(coral_name):
    obj = bpy.data.objects[coral_name]  # Replace coral_name with the actual name of your coral model
    bbox = obj.bound_box  # Bounding box vertices
    x_extent = max([v[0] for v in bbox]) - min([v[0] for v in bbox])
    y_extent = max([v[1] for v in bbox]) - min([v[1] for v in bbox])
    return max(x_extent, y_extent) / 2

for coral_name in species_abundance.keys():
    if coral_name in coral_models:
        # Load each coral model (all variations for each species)
        coral_filepaths = coral_models[coral_name]
        loaded_coral_objects[coral_name] = []
        
        for filepath in coral_filepaths:
            bpy.ops.wm.obj_import(filepath=filepath)
            loaded_coral = bpy.context.view_layer.objects[-1] 
            loaded_coral_objects[coral_name].append(loaded_coral)
            # Hide the loaded coral models
            loaded_coral.hide_set(True)  

class Coral:
    def __init__(self, species, clustering_factor):
        self.species = species
        if species not in loaded_coral_objects:
            print(f"Warning: No models found for coral {species}")
            sys.exit(1)
        
        # Select and link a coral model to the scene
        self.model = random.choice(loaded_coral_objects[species]).copy()
        self.model.data = random.choice(loaded_coral_objects[species]).data  # Share mesh data for instancing
        bpy.context.collection.objects.link(self.model)

        # Apply random Z-axis rotation
        z_rotation = random.uniform(0, 2 * math.pi)
        self.model.rotation_euler = (math.pi / 2, 0, z_rotation)
        
        self.clustering_factor = clustering_factor
        bpy.context.view_layer.update()  # Ensure transformations are applied

    def get_bb_corners(self):
        """Retrieve the world-space bounding box corners of the model."""
        return [self.model.matrix_world @ Vector(corner) for corner in self.model.bound_box]

def is_position_clear(coral, placed_instances, padding=0.1):
    coral_bb = coral.get_bb_corners()  # Get transformed bounding box corners of current coral
    for placed in placed_instances:
        placed_bb = placed['bb_corners']  # Transformed bounding box corners of already placed corals
        if bounding_boxes_overlap(coral_bb, placed_bb, padding):
            return False
    return True

def bounding_boxes_overlap(bb1, bb2, padding=0.1):
    bb1_min = [min(c[i] for c in bb1) - padding for i in range(3)]
    bb1_max = [max(c[i] for c in bb1) + padding for i in range(3)]
    bb2_min = [min(c[i] for c in bb2) - padding for i in range(3)]
    bb2_max = [max(c[i] for c in bb2) + padding for i in range(3)]
    # Check for overlap in all three axes (x, y, and z)
    return all(bb1_min[i] <= bb2_max[i] and bb1_max[i] >= bb2_min[i] for i in range(3))

def create_bb_visualization(coral_instance):
    """Visualize the bounding box for the coral model."""
    # Create a mesh for the bounding box
    bb_corners = coral_instance.get_bb_corners()
    mesh_data = bpy.data.meshes.new(f"BB_Mesh_{coral_instance.species}")
    bb_obj = bpy.data.objects.new(f"BB_{coral_instance.species}", mesh_data)
    bpy.context.collection.objects.link(bb_obj)
    
    # Create bounding box vertices and edges
    vertices = [(v.x, v.y, v.z) for v in bb_corners]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    mesh_data.from_pydata(vertices, edges, [])
    mesh_data.update()
    
    # Display as wireframe
    bb_obj.display_type = 'WIRE'
    bb_obj.show_in_front = True  # Draw in front of other objects
    return bb_obj

# Initialize corals list
corals = []
for coral_name in species_abundance.keys():
    for _ in range(species_abundance[coral_name]):
        corals.append(Coral(coral_name, 0))

random.shuffle(corals)
placed_instances = []

# Define terrain boundaries (adjust these based on terrain)
terrain_min_x, terrain_max_x = 0, 10
terrain_min_y, terrain_max_y = 0, 10

# Set up a spatial grid to partition the area and limit the collision check range
grid_size = 1.0  # Size of each grid cell, adjust based on coral model dimensions
spatial_grid = {}

def get_grid_key(x, y):
    """Compute grid key based on x, y coordinates."""
    return (int(x // grid_size), int(y // grid_size))

def add_to_spatial_grid(coral, key):
    """Add coral to spatial grid for faster lookups."""
    if key not in spatial_grid:
        spatial_grid[key] = []
    spatial_grid[key].append(coral)

def is_position_clear_optimized(coral, placed_instances, padding=0.1):
    """Optimized version to check if the coral’s bounding box overlaps."""
    coral_bb = coral.get_bb_corners()
    key = get_grid_key(coral.model.location.x, coral.model.location.y)

    # Only check nearby cells in the spatial grid
    nearby_cells = [
        (key[0] + dx, key[1] + dy)
        for dx in range(-1, 2)
        for dy in range(-1, 2)
    ]

    for cell in nearby_cells:
        if cell in spatial_grid:
            for placed in spatial_grid[cell]:
                placed_bb = placed['bb_corners']
                if bounding_boxes_overlap(coral_bb, placed_bb, padding):
                    return False
    return True

for coral in corals:
    max_attempts = 100
    attempts = 0
    placed = False

    while attempts < max_attempts and not placed:
        x = random.uniform(terrain_min_x, terrain_max_x)
        y = random.uniform(terrain_min_y, terrain_max_y)
        z = get_terrain_height(x, y)

        # Set location and rotation, call update only once per coral
        coral.model.location = (x, y, z)
        bpy.context.view_layer.update()  # Minimize calls to update

        # Check position with optimized spatial grid
        if is_position_clear_optimized(coral, placed_instances, padding=0.1):
            # Ensure coral is not linked to any collection before adding to avoid duplicate linking
            if not coral.model.users_collection:
                bpy.context.collection.objects.link(coral.model)
                
            placed_instances.append({
                'instance': coral.model,
                'bb_corners': coral.get_bb_corners()
            })

            # Add coral to spatial grid
            add_to_spatial_grid(placed_instances[-1], get_grid_key(x, y))

            # Visualize bounding box
            create_bb_visualization(coral)
            placed = True

        attempts += 1

    # Remove unplaced corals to avoid clutter in the scene
    if not placed:
        print(f"Warning: Could not place coral '{coral.species}' after {max_attempts} attempts.")
        bpy.data.objects.remove(coral.model, do_unlink=True)

print(f"Successfully placed {len(placed_instances)} out of {len(corals)} corals.")

# Export the blender file!
bpy.ops.wm.save_as_mainfile(filepath="output_scene.blend")

print("Blender scene created and saved successfully.")