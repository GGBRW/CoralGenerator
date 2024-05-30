''' 
The requirements for CFD compatible mesh would be including but not limited to

* Watertight mesh of either obj or stl format
* No sharp triangles or flat topology of the mesh. Ideally avoid highly skewed triangles.
* Try to limit the total size of the file below 1GiB for memory optimisation

'''

import numpy as np
import pyvista as pv
import os

def check_mesh(file_path):
    if not os.path.isfile(file_path):
        print("File does not exist.")
        return

    # Check if the file size is too large
    file_size = os.path.getsize(file_path) / (1024 * 1024 * 1024)
    if file_size >= 1:
        print("Warning: File size is too large (>1GiB).")
    

    mesh = pv.read(file_path)
    
    # Check for watertightness
    if mesh.is_all_triangles:
        edges = mesh.extract_feature_edges(non_manifold_edges=True, boundary_edges=True, feature_edges=False)
        if edges.n_cells > 0:
            print("Mesh is not watertight.")
        else:
            print("Mesh is watertight.")
    else:
        print("Mesh does not consist of all triangles.")
    
    # Check for quality of triangles
    quality = mesh.compute_cell_quality(quality_measure='scaled_jacobian')
    min_quality = quality.cell_data['CellQuality'].min()
    
    if min_quality < 0.1:
        print("Mesh contains highly skewed triangles.")
    else:
        print("Triangle quality is acceptable.")
    
    return

# file_path = 'path_to_your_mesh.obj'
# check_mesh(file_path)
