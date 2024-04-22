# This script imports all the coral .obj files in the Blender scene.

import bpy

objs = [
  'usnm_74016-100k-2048-obj_std/usnm_74016-150k.obj',
  'usnm_1171477-100k-2048-obj_std/usnm_1171477-150k.obj',
  'usnm_3968-100k-2048-obj_std/usnm_3968-150k.obj',
  'usnm_1149322-100k-2048-obj_std/usnm_1149322-150k.obj',
  'usnm_47056-100k-4096-obj_std/usnm_47056-150k.obj',
  'usnm_58-100k-2048-obj_std/usnm_58-150k.obj',
  'usnm_56807-100k-2048-obj_std/usnm_56807-150k.obj',
  'usnm_1246330-100k-4096-obj_std/usnm_1246330-150k.obj',
  'usnm_74947-100k-2048-obj_std/usnm_74947-150k.obj',
  'usnm_1122878-100k-2048-obj_std/usnm_1122878-150k.obj',
  'usnm_76340-100k-2048-obj_std/usnm_76340-150k.obj',
  'usnm_164-100k-2048-obj_std/usnm_164-150k.obj',
  'usnm_210-100k-2048-obj_std/usnm_210-150k.obj',
  'usnm_91274-100k-2048-obj_std/usnm_91274-150k.obj',
  'usnm_91201-100k-2048-obj_std/usnm_91201-150k.obj',
  'usnm_5781-100k-2048-obj_std/usnm_5781-150k.obj',
  'usnm_1145291-100k-2048-obj_std/usnm_1145291-150k.obj',
  'usnm_160-100k-2048-obj_std/usnm_160-150k.obj',
  'usnm_83771-100k-2048-obj_std/usnm_83771-150k.obj',
  'usnm_83788-100k-2048-obj_std/usnm_83788-150k.obj',
  'usnm_93447-100k-2048-obj_std/usnm_93447-150k.obj',
  'usnm_285-100k-2048-obj_std/usnm_285-150k.obj',
  'usnm_240-100k-2048-obj_std/usnm_240-150k.obj',
  'usnm_229-100k-2048-obj_std/usnm_229-150k.obj',
  'usnm_282-100k-2048-obj_std/usnm_282-150k.obj',
  'usnm_292-100k-2048-obj_std/usnm_292-150k.obj',
  'usnm_291-100k-2048-obj_std/usnm_291-150k.obj',
  'usnm_332-100k-2048-obj_std/usnm_332-150k.obj',
  'usnm_246-100k-2048-obj_std/usnm_246-150k.obj',
  'usnm_297-100k-2048-obj_std/usnm_297-150k.obj',
  'usnm_244-100k-2048-obj_std/usnm_244-150k.obj',
  'usnm_251-100k-2048-obj_std/usnm_251-150k.obj',
  'usnm_272-100k-2048-obj_std/usnm_272-150k.obj',
  'usnm_335-100k-2048-obj_std/usnm_335-150k.obj',
  'usnm_312-100k-2048-obj_std/usnm_312-150k.obj',
  'usnm_336-100k-2048-obj_std/usnm_336-150k.obj',
  'usnm_317-100k-2048-obj_std/usnm_317-150k.obj',
  'usnm_318-100k-2048-obj_std/usnm_318-150k.obj',
  'usnm_1174917-100k-2048-obj_std/usnm_1174917-150k.obj',
  'usnm_148-100k-2048-obj_std/usnm_148-150k.obj',
  'usnm_1494038-100k-2048-obj_std/usnm_1494038-150k.obj',
  'usnm_307-100k-2048-obj_std/usnm_307-150k.obj',
  'usnm_201-100k-2048-obj_std/usnm_201-150k.obj',
  'usnm_44359-100k-2048-obj_std/usnm_44359-150k.obj',
  'usnm_81450-100k-2048-obj_std/usnm_81450-150k.obj',
  'usnm_46926-100k-2048-obj_std/usnm_46926-150k.obj',
  'usnm_1128565-100k-2048-obj_std/usnm_1128565-150k.obj',
  'usnm_93379-100k-2048-obj_std/usnm_93379-150k.obj',
  'usnm_700-100k-2048-obj_std/usnm_700-150k.obj',
  'usnm_89696-100k-2048-obj_std/usnm_89696-150k.obj',
  'usnm_20994-100k-2048-obj_std/usnm_20994-150k.obj',
  'usnm_20996-100k-2048-obj_std/usnm_20996-150k.obj',
  'usnm_646-100k-2048-obj_std/usnm_646-150k.obj',
  'usnm_664-100k-2048-obj_std/usnm_664-150k.obj',
  'usnm_188-100k-2048-obj_std/usnm_188-150k.obj',
  'usnm_1137708-100k-4096-obj_std/usnm_1137708-150k.obj',
  'usnm_79493-100k-2048-obj_std/usnm_79493-150k.obj',
  'usnm_344-100k-2048-obj_std/usnm_344-150k.obj',
  'usnm_1122454-100k-2048-obj_std/usnm_1122454-150k.obj',
  'usnm_1122540-100k-2048-obj_std/usnm_1122540-150k.obj',
  'usnm_76600-100k-2048-obj_std/usnm_76600-150k.obj',
  'usnm_1027819-100k-2048-obj_std/usnm_1027819-150k.obj',
  'usnm_558-100k-2048-obj_std/usnm_558-150k.obj',
  'usnm_346-100k-obj/usnm_346-01-100k.obj'
]

pref = "/Users/ggbrw/Documents/GEO Thesis/CoralGeneratorRepo/Smithsonian Corals scripts/filtered_corals/"

def import_obj(file_path):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    bpy.ops.wm.obj_import(filepath=file_path)

    
import_obj(pref + objs[0])