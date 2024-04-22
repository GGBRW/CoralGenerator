# This script aligns the corals to (0,0,0) with the lowest point of the coral at y=0.

import bpy
import bmesh

obj = bpy.context.object
bpy.ops.object.mode_set(mode='OBJECT')

bm = bmesh.new()
bm.from_mesh(obj.data)

lowest_y = min(v.co.y for v in bm.verts)

new_origin = obj.location.x, obj.location.y + lowest_y, obj.location.z

for v in bm.verts:
    v.co.y -= lowest_y

bm.to_mesh(obj.data)
bm.free()
obj.data.update()
