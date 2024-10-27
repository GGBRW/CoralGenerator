import bpy
import bmesh
import math
import mathutils
from mathutils import noise
import json
import random
import numpy as np
import os
import sys

# Always the first thing to do when working with Blender, remove the 'default cube' :)
bpy.ops.wm.read_factory_settings(use_empty=True)

# PARAMETERS FOR TERRAIN GENERATION (fBm)
overall_slope = math.radians(30)      # Overall slope of the terrain (in radians)
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

total_abundance = 1000
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

# Spatial distribution of species
if calculate_spatial_distribution:
    print("Calculating spatial distribution...")
    spatial_distribution = generate_spatial_distribution.calculate_spatial_distribution(species_abundance)
else:
    with open(spatial_distribution_file, 'r') as f:
        spatial_distribution = json.load(f)

# Distribute corals based on the spatial distribution data
for colony in spatial_distribution:
    coral_name = colony['species']
    x = colony['x']
    y = colony['y']

    if coral_name not in loaded_coral_objects:
        print(f"Warning: No models found for coral {coral_name}")
        continue
    
    # Pick a random model for this coral
    coral_variants = loaded_coral_objects[coral_name]
    coral_model = random.choice(coral_variants)
    
    # Create an INSTANCE of the coral model
    coral_instance = coral_model.copy()
    coral_instance.data = coral_model.data  # Share the same mesh data (instancing)
    bpy.context.collection.objects.link(coral_instance)

    # Position coral based on spatial distribution coordinates
    z = get_terrain_height(x, y)
    coral_instance.location = (x, y, z)

    # Random Z-axis rotation
    z_rotation = random.uniform(0, 2 * math.pi)
    coral_instance.rotation_euler = (math.pi / 2, 0, z_rotation)

# Export the blender file!
bpy.ops.wm.save_as_mainfile(filepath="output_scene.blend")

print("Blender scene created and saved successfully.")