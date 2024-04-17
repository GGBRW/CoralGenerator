import json
import trimesh
import random
import numpy as np

def create_terrain(size=10, subdivisions=4):
    step = size / subdivisions
    vertices = []
    faces = []
    for i in range(subdivisions + 1):
        for j in range(subdivisions + 1):
            vertices.append([i * step - size / 2, 0, j * step - size / 2])
    for i in range(subdivisions):
        for j in range(subdivisions):
            start = i * (subdivisions + 1) + j
            faces.append([start, start + 1, start + subdivisions + 2])
            faces.append([start, start + subdivisions + 2, start + subdivisions + 1])
    return trimesh.Trimesh(vertices=vertices, faces=faces)

with open('coral_catalog.json') as f:
    data = json.load(f)
    
    meshes = []

    # Ensure random index is within the list bounds
    for i in range(10):
        ix = random.randint(0, len(data) - 1)
        fp = data[ix]['filepath']
        meshes.append(trimesh.load(fp))

        print("loaded mesh from", data[ix]["name"], " | ", fp)

    # Create a plane to serve as terrain
    terrain = create_terrain()

    # Distribute the meshes over the terrain
    for i in range(20):
        # Generate random x, y coordinates within the extents of the terrain
        x = random.uniform(-5, 5)
        y = random.uniform(-5, 5)

        # Create a translation matrix to move the mesh to the random (x, y) location
        translation = trimesh.transformations.translation_matrix([x, 0, y])

        ix = random.randint(0, len(meshes) - 1)
        mesh = meshes[ix]
        # Apply the translation to the mesh
        mesh.apply_transform(translation)

        # Optionally, you can merge all meshes into one for unified processing or visualization
    # Combine all meshes with the terrain into a single mesh
    combined_mesh = trimesh.util.concatenate([terrain] + meshes)

    # Optionally, display the combined mesh if you are in an environment that supports visualization
    # combined_mesh.show()

    # write to obj file 
    combined_mesh.export('combined_mesh.obj')

