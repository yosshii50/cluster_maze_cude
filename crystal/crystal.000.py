import bpy
import bmesh

# 既存のオブジェクトをすべて削除（任意）
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# UV Sphere を追加
bpy.ops.mesh.primitive_uv_sphere_add(segments=4,ring_count=4,radius=1.0,location=(0, 0, 0))

obj = bpy.context.object
bpy.ops.object.mode_set(mode='EDIT')
mesh = bmesh.from_edit_mesh(obj.data)

#print(len(mesh.edges))
# 28個

#for e in mesh.edges:
#    e.select = False

"""
# 条件に合う辺だけ選択（例: 長さがしきい値より短いものを削除）
threshold_st = 0.99
threshold_ed = 1.01
for edge in mesh.edges:
    if edge.calc_length() > threshold_st and edge.calc_length() < threshold_ed:
        edge.select = True
    else:
        edge.select = False
"""

for edge in mesh.edges:
    if edge.calc_length() > 0.99 and edge.calc_length() < 1.01:
        edge.select = True
    else:
        edge.select = False

#for edge in mesh.edges:
#    print(edge.calc_length())


bmesh.ops.dissolve_edges(mesh, edges=[e for e in mesh.edges if e.select], use_verts=True)
#bmesh.ops.dissolve_edges(mesh, edges=[mesh.edges[0]], use_verts=False)
#bmesh.ops.dissolve_edges(mesh, edges=[mesh.edges[0],mesh.edges[1]], use_verts=False)

bmesh.update_edit_mesh(obj.data, loop_triangles=True)
bpy.ops.object.mode_set(mode='OBJECT')


##############################################################################################################################
# ブロックの作成
##############################################################################################################################


scale_xyz = (1 / 3) / 2
bpy.ops.mesh.primitive_cube_add(scale=(scale_xyz, scale_xyz, scale_xyz)) # キューブ作成

