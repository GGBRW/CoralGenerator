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

with open('CORALCATALOG.json') as f:
    data = json.load(f)
    data = [x for x in data if not "notes" in x]
    
    meshes = []
    for i in range(10):
        ix = random.randint(0, len(data) - 1)
        fp = "filtered_corals/" + data[ix]['filepath']
        fp = fp.replace(".obj", "_adj.obj")
        mesh = trimesh.load(fp)

        x = random.uniform(-1.25, 1.25)
        y = random.uniform(-1.25, 1.25)
        translation = trimesh.transformations.translation_matrix([x, 0, y])
        mesh.apply_transform(translation)

        meshes.append(mesh)

        print("loaded mesh from", data[ix]["name"], " | ", fp)

    terrain = create_terrain(2.5, 5)

    combined_mesh = trimesh.util.concatenate([terrain] + meshes)

    # write to obj file 
    combined_mesh.export('combined_mesh.obj')

