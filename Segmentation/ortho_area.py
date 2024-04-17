import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def load_obj(filename):
    """Load vertices and faces from an OBJ file."""
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts:
                if parts[0] == 'v':
                    vertices.append([float(parts[1]), float(parts[3]), float(parts[2])])
                elif parts[0] == 'f':
                    faces.append([int(i.split('/')[0]) - 1 for i in parts[1:]])
    return np.array(vertices), faces

def project_faces(vertices, faces):
    """Create 2D polygons for each face by projecting 3D vertices onto a 2D plane."""
    polygons = []
    for face in faces:
        polygon = vertices[face][:, :2]  
        polygons.append(Polygon(polygon, True))
    return polygons

def plot_and_estimate_area(polygons):
    """Plot 2D polygons and estimate the area covered by them."""
    fig, ax = plt.subplots()
    p = PatchCollection(polygons, alpha=0.4)
    ax.add_collection(p)
    plt.axis('equal')
    plt.show()

    all_points = np.concatenate([p.get_xy() for p in polygons])
    min_x, min_y = np.min(all_points, axis=0)
    max_x, max_y = np.max(all_points, axis=0)
    estimated_area = (max_x - min_x) * (max_y - min_y)
    
    return estimated_area

# vertices, faces = load_obj('corals/cervicornis.obj')
vertices, faces = load_obj('corals.obj')

polygons = project_faces(vertices, faces)

estimated_area = plot_and_estimate_area(polygons)
print(f"Estimated projected area: {estimated_area} units²")
