import bpy
import bmesh
from itertools import product

# クリスタル作成
def create_sphere(radius):
    #radius=(1/3)/2
    #radius=(1/3)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=4,ring_count=4,radius=radius,location=(0, 0, 0.5))
    obj = bpy.context.object
    bpy.ops.object.mode_set(mode='EDIT')
    mesh = bmesh.from_edit_mesh(obj.data)
    threshold_st = 0.99 * radius
    threshold_ed = 1.01 * radius
    for edge in mesh.edges:
        if edge.calc_length() > threshold_st and edge.calc_length() < threshold_ed:
            edge.select = True
        else:
            edge.select = False
    bmesh.ops.dissolve_edges(mesh, edges=[e for e in mesh.edges if e.select], use_verts=True)
    bmesh.update_edit_mesh(obj.data, loop_triangles=True)
    bpy.ops.object.mode_set(mode='OBJECT')

# ブロックの作成
def create_cube():
    scale_xyz = (1 / 3) / 2
    bpy.ops.mesh.primitive_cube_add(scale=(scale_xyz, scale_xyz, scale_xyz)) # キューブ作成

# 6面のUV座標を設定
def set_obj_alluv(obj_uv_layer, use_uv_line_no):
    # 1面のuvマッピングを設定
    def set_obj_faceuv(obj_uv_layer,face_no,xpos,ypos):
        face_pos = face_no * 4
        obj_uv_layer[face_pos + 0].uv.x = (xpos + 1) * (21/256)
        obj_uv_layer[face_pos + 1].uv.x = (xpos + 0) * (21/256)
        obj_uv_layer[face_pos + 2].uv.x = (xpos + 0) * (21/256)
        obj_uv_layer[face_pos + 3].uv.x = (xpos + 1) * (21/256)
        obj_uv_layer[face_pos + 0].uv.y = 256- (ypos + 0) * (21/256)
        obj_uv_layer[face_pos + 1].uv.y = 256- (ypos + 0) * (21/256)
        obj_uv_layer[face_pos + 2].uv.y = 256- (ypos + 1) * (21/256)
        obj_uv_layer[face_pos + 3].uv.y = 256- (ypos + 1) * (21/256)
    for face_no in range(6):
        set_obj_faceuv(obj_uv_layer, face_no, face_no, use_uv_line_no)

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
    tex_image.image = bpy.data.images.load("D:\\Cluster\\ControlBox\\crystal\\maze_crystal_image.png")
    tex_image.interpolation = 'Closest'
    # 画像ノードをBSDFのベースカラーに接続
    links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
    return mat

def create_cube_one(cube_x, cube_y, cube_z, mat):
    use_uv_line_no = cube_x + cube_y * 2 + cube_z * 4
    #print(use_uv_line_no)
    scale_xyz = (1 / 3) / 2
    bpy.ops.mesh.primitive_cube_add(scale=(scale_xyz, scale_xyz, scale_xyz), location=(cube_x, cube_y, cube_z)) # キューブ作成
    this_obj = bpy.context.active_object
    this_obj.name = "Cube" + str(cube_x) + str(cube_y) + str(cube_z)
    #this_obj.data.materials[0] = mat
    this_obj.data.materials.append(mat)
    uv_layer_b = this_obj.data.uv_layers.active.data
    set_obj_alluv(uv_layer_b, use_uv_line_no)

##############################################################################################################################
##############################################################################################################################

# 既存のオブジェクトをすべて削除（任意）
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# マテリアル作成
mat = create_material()

create_sphere(1/3)
create_sphere( ( 1/3 ) * 0.5)
#create_cube()
create_cube_one(0, 0, 0, mat)
