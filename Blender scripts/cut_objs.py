import bpy
import json 
import bmesh
import os


coral_index = 12
coral_dir = "/Users/ggbrw/Documents/GEO Thesis/CoralGeneratorRepo/Smithsonian Corals scripts/filtered_corals/"
catalog = load_catalog()

def import_obj(file_path, clear_scene=True):
    # Optional: remove all object in the scene first
    if clear_scene:
        scene = bpy.context.scene
        for obj in scene.objects:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
        bpy.ops.object.delete()

    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    bpy.ops.wm.obj_import(filepath=file_path)
    

def export_obj(filepath):
    # Get the currently selected object
    selected_object = bpy.context.active_object

    # Ensure the object is selected
    selected_object.select_set(True)

    # Set the path where the OBJ file will be saved
    if not filepath:
        print("No filepath provided.")
        return

    # Ensure the path ends with '.obj'
    if not filepath.lower().endswith('.obj'):
        filepath += '.obj'

    # Export the selected object as an OBJ file
    bpy.ops.wm.obj_export(
        filepath=filepath,
        check_existing=True,
        filter_folder=True,
        filemode=8,
        display_type='DEFAULT',
        sort_method='DEFAULT',
        export_animation=False,
        forward_axis='NEGATIVE_Z',
        up_axis='Y',
        global_scale=1,
        apply_modifiers=True,
        export_eval_mode='DAG_EVAL_VIEWPORT',
        export_selected_objects=True,
        export_uv=True,
        export_normals=True,
        export_materials=True,
        path_mode='AUTO'
    )
    print(f"Exported '{selected_object.name}' to '{filepath}'.")
    
def add_boolean_cube():
    obj = bpy.context.active_object
    
    bpy.ops.mesh.primitive_cube_add()
    cube = bpy.context.object
    cube.name = "BooleanCube"
    
    boolean_modifier = obj.modifiers.new(name="NewBoolean", type='BOOLEAN')
    boolean_modifier.operation = 'DIFFERENCE'
    boolean_modifier.object = cube
    
    cube.scale = (.1, .1, .1)
    cube.location.z -= .2
    
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    cube.select_set(False)
    
def apply_boolean_cube():
    obj = bpy.context.active_object
    
    cube = bpy.data.objects.get("BooleanCube")
    z_top = cube.location.z + 0.5 * cube.dimensions.z
    
    print(f"Cutoff coral at {z_top}")
    
    obj.modifiers.get("NewBoolean")
    bpy.ops.object.modifier_apply(modifier="NewBoolean")
    
    
    
def align_z_with_terrain():
    obj = bpy.context.object
    bpy.ops.object.mode_set(mode='OBJECT')

    bm = bmesh.new()
    bm.from_mesh(obj.data)

    lowest_y = min(v.co.y for v in bm.verts)

    new_origin = obj.location.x, obj.location.y + lowest_y, obj.location.z

    for v in bm.verts:
        v.co.y -= lowest_y
        
    print(f"moved all vertices {-lowest_y}")

    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    
def load_catalog():
    file = open("/Users/ggbrw/Documents/GEO Thesis/CoralGeneratorRepo/Smithsonian Corals scripts/CORALCATALOG.json")
    catalog = json.load(file)
    return catalog

def load_coral(ix):
    import_obj(coral_dir + catalog[ix]["filepath"])