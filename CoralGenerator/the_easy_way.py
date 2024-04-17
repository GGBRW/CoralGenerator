import numpy as np
import trimesh
import noise
import random

# Terrain parameters
terrain_width = 4
terrain_height = 4
terrain_vertices_x = 64
terrain_vertices_y = 64

# Noise parameters
noise_frequencies = [0.35, 0.5, 1.5]
noise_amplitudes = [1.5, 1.0, 0.2]
noise_seed = 0

def calculate_terrain_height(x, y):
    z = 0.0
    for freq, amp in zip(noise_frequencies, noise_amplitudes):
        z += amp * noise.pnoise2(freq * x, freq * y, base=noise_seed)
    return z

# Generate terrain
vertices = []
faces = []
for i in range(terrain_vertices_x):
    for j in range(terrain_vertices_y):
        x = i * terrain_width / terrain_vertices_x
        y = j * terrain_height / terrain_vertices_y
        z = calculate_terrain_height(x, y)
        vertices.append([x, z, y])  # Swapping y and z to match OBJ coordinate system

# Create faces for the terrain
for i in range(terrain_vertices_x - 1):
    for j in range(terrain_vertices_y - 1):
        top_left = i * terrain_vertices_y + j
        top_right = (i + 1) * terrain_vertices_y + j
        bottom_left = i * terrain_vertices_y + (j + 1)
        bottom_right = (i + 1) * terrain_vertices_y + (j + 1)
        faces.append([top_left, bottom_left, bottom_right])
        faces.append([top_left, bottom_right, top_right])

terrain_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

print("Terrain mesh has {} vertices and {} faces".format(len(terrain_mesh.vertices), len(terrain_mesh.faces)))

# Load coral meshes (replace with paths to your coral OBJ files)
coral_filepaths = ["corals/cervicornis.obj", "corals/secale.obj"]
coral_meshes = [trimesh.load(filepath) for filepath in coral_filepaths]

print("Loaded {} coral meshes".format(len(coral_meshes)))

# Place corals
num_corals = 8
for _ in range(num_corals):
    coral_mesh = random.choice(coral_meshes).copy()

    # Random position on the terrain
    x = random.uniform(0, terrain_width)
    y = calculate_terrain_height(x, random.uniform(0, terrain_height))
    z = random.uniform(0, terrain_height)

    print("Placing coral at ({}, {}, {})".format(x, y, z))
    
    # Random rotation around the Y-axis
    angle = random.uniform(0, 2 * np.pi)
    rotation = trimesh.transformations.rotation_matrix(angle, [0, 1, 0])
    translation = trimesh.transformations.translation_matrix([x, y, z])
    transform = np.dot(translation, rotation)

    coral_mesh.apply_transform(transform)
    terrain_mesh += coral_mesh

# Export the combined mesh
terrain_mesh.export('combined_terrain_corals.obj')
