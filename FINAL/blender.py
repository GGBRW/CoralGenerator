import bpy
import bmesh
import math
import mathutils
from mathutils import noise
import json
import random
import numpy as np

# Remove the 'default cube' :)
bpy.ops.wm.read_factory_settings(use_empty=True)

# PARAMETERS FOR TERRAIN GENERATION (FbM)
terrain_size = 100  # Number of grid points (both x and y)
grid_extent = 10.0  # Total size of the grid in meters (10x10 meters)
grid_spacing = grid_extent / (terrain_size - 1)  # Spacing between points
octaves = 6         # The number of layers of noise (controls fractal detail)
persistence = 0.5   # Controls the amplitude of each octave
lacunarity = 2.0    # Controls the frequency of each octave
scale = 50.0        # Scaling factor for the noise (can adjust based on preference)
height_amplification = 1.0  # Amplify the height variation if necessary

# INPUT: species abundance (corals to distribute)
total_abundance = 1000
coral_distribution = {
    "Pocillopora grandis": 0.03804347826086957,
    "Porites lobata": 0.10869565217391304,
    "Acropora hyacinthus": 0.005434782608695652,
    "Acropora robusta": 0.03260869565217391,
    "Pocillopora meandrina": 0.03804347826086957,
    "Psammocora columna": 0.03804347826086957,
    "Herpolitha limax": 0.07065217391304347,
    "Echinopora lamellosa": 0.03804347826086957,
    "Astrea curta": 0.2391304347826087,
    "Hydnophora rigida": 0.05434782608695652,
    "Acropora cervicornis": 0.010869565217391304,
    "Distichopora violacea": 0.07608695652173914,
    "Acropora valenciennesi": 0.010869565217391304,
    "Pocillopora damicornis": 0.07065217391304347,
    "Homophyllia australis": 0.010869565217391304,
    "Stylophora pistillata": 0.010869565217391304,
    "Heliopora coerulea": 0.016304347826086956,
    "Acropora florida": 0.005434782608695652,
    "Seriatopora hystrix": 0.005434782608695652,
    "Acropora valida": 0.010869565217391304,
    "Montipora digitata": 0.010869565217391304,
    "Montipora caliculata": 0.09782608695652174
}

for coral_name, count in coral_distribution.items():
    coral_distribution[coral_name] = round(count * total_abundance)

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
        
        # Generate the z-coordinate (height) using the fBm function
        z = fbm(i / scale, j / scale, octaves, persistence, lacunarity) * height_amplification
        
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


# Helper function to get the closest terrain height
def get_terrain_height(x_pos, y_pos):
    # Find the closest grid points
    grid_x = int(x_pos / grid_spacing)
    grid_y = int(y_pos / grid_spacing)
    
    if 0 <= grid_x < terrain_size and 0 <= grid_y < terrain_size:
        return terrain_heights[grid_x][grid_y]
    return 0.0 

# Load necessary coral models (only once)
loaded_coral_objects = {}

for coral_name in coral_distribution.keys():
    if coral_name in coral_models:
        # Load each coral model (all variations)
        coral_filepaths = coral_models[coral_name]
        loaded_coral_objects[coral_name] = []
        
        for filepath in coral_filepaths:
            bpy.ops.wm.obj_import(filepath=filepath)
            loaded_coral = bpy.context.view_layer.objects[-1] 
            loaded_coral_objects[coral_name].append(loaded_coral)

# Distribute coral instances across the terrain
for coral_name, count in coral_distribution.items():
    if coral_name not in loaded_coral_objects:
        print(f"Warning: No models found for coral {coral_name}")
        continue
    
    # Get all the loaded models for this coral
    coral_variants = loaded_coral_objects[coral_name]
    
    for _ in range(count):
        # Pick a random model for this coral
        coral_model = random.choice(coral_variants)
        
        # Create an INSTANCE of the coral model
        coral_instance = coral_model.copy()
        coral_instance.data = coral_model.data  # Share the same mesh data (instancing)
        bpy.context.collection.objects.link(coral_instance)

        # CSR
        x = random.uniform(0, grid_extent)
        y = random.uniform(0, grid_extent)
        z = get_terrain_height(x, y)
        
        coral_instance.location = (x, y, z)

        # Random Z-axis rotation
        z_rotation = random.uniform(0, 2 * math.pi)
        coral_instance.rotation_euler = (math.pi / 2, 0, z_rotation)

# Export the blender file!
bpy.ops.wm.save_as_mainfile(filepath="output_scene.blend")

print("Blender scene created and saved successfully.")
