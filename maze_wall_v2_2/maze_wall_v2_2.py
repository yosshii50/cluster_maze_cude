"""
"""

import bpy

# マテリアル作成
def create_material():
    # マテリアルを新規作成
    mat = bpy.data.materials.new(name="MyMaterial")
    mat.use_nodes = True
    # ノードツリーにアクセス
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    # デフォルトのプリンシプルBSDFを取得
    bsdf = nodes.get("Principled BSDF")
    # 画像テクスチャノードを作成
    tex_image = nodes.new('ShaderNodeTexImage')
    # 画像をロード
    tex_image.image = bpy.data.images.load("D:\\Cluster\\ControlBox\\maze_wall_v2_2\\maze_combined4.png")
    # 画像ノードをBSDFのベースカラーに接続
    links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
    return mat

# マテリアル作成
mat = create_material()

# 一度すべてのオブジェクトを削除
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 1x1のPlaneを作成
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
plane = bpy.context.active_object
plane.scale = (2, 1, 1)  # 1x2に調整

plane.data.materials.append(mat)
obj_uv_layer = plane.data.uv_layers.active.data

def set_obj_faceuv(obj_uv_layer,xpos1,ypos1):
    xpos2 = xpos1 + 2
    ypos2 = ypos1 + 2
    obj_uv_layer[0].uv.x = (xpos2 + 4) * (21/256)
    obj_uv_layer[1].uv.x = (xpos1 + 0) * (21/256)
    obj_uv_layer[2].uv.x = (xpos1 + 0) * (21/256)
    obj_uv_layer[3].uv.x = (xpos2 + 4) * (21/256)
    obj_uv_layer[0].uv.y = 256- (ypos1 + 0) * (21/256)
    obj_uv_layer[1].uv.y = 256- (ypos1 + 0) * (21/256)
    obj_uv_layer[2].uv.y = 256- (ypos2 + 1) * (21/256)
    obj_uv_layer[3].uv.y = 256- (ypos2 + 1) * (21/256)
    

set_obj_faceuv(obj_uv_layer, 0, 0)
