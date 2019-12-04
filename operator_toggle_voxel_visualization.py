import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    PointerProperty,
    StringProperty,
    BoolProperty,
)


def plane_data(scale=1.0):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """

    verts = [
        (+1.0, +1.0, 0.0),
        (+1.0, -1.0, 0.0),
        (-1.0, -1.0, 0.0),
        (-1.0, +1.0, 0.0),
    ]

    faces = [
        (0, 1, 2, 3),
    ]

    # apply size
    for i, v in enumerate(verts):
        verts[i] = v[0] * scale, v[1] * scale, v[2]

    return verts, faces


def plane_mesh():
    if "VoxelPlaneMesh" in bpy.data.meshes and len(bpy.data.meshes["VoxelPlaneMesh"].vertices) > 0:
        return bpy.data.meshes["VoxelPlaneMesh"]

    verts_loc, faces = plane_data()
    mesh = bpy.data.meshes.new("VoxelPlaneMesh")

    bm = bmesh.new()

    for v_co in verts_loc:
        bm.verts.new(v_co)

    bm.verts.ensure_lookup_table()
    for f_idx in faces:
        bm.faces.new([bm.verts[i] for i in f_idx])

    bm.to_mesh(mesh)
    mesh.update()

    return mesh


class ToggleVoxelVisualization(bpy.types.Operator):
    """Toggle voxel visualization for a tile"""
    bl_idname = "tyler.toggle_voxel_visualization"
    bl_label = "Toggle Voxel Visualization"
    bl_options = {'REGISTER', 'UNDO'}

    is_visible: BoolProperty(
        name="Is Visible"
    )
    tile_name: StringProperty(
        name="Tile name",
    )

    def execute(self, context):
        if self.tile_name in context.collection.objects:
            pass
        else:
            return {'CANCELLED'}

        active_collection = context.view_layer.active_layer_collection.collection
        tile_obj = context.collection.objects[self.tile_name]

        if len(tile_obj.children) > 0:
            for child in tile_obj.children:
                for grand_child in child.children:
                    grand_child.hide_viewport = self.is_visible == False
            return {'FINISHED'}

        name = self.tile_name + '.voxel_viz'
        empty_mesh_data = bpy.data.meshes.new("hey")
        voxel_viz = bpy.data.objects.new(name, empty_mesh_data)
        active_collection.objects.link(voxel_viz)
        voxel_viz.parent = tile_obj
        voxel_viz.lock_rotation = (True, True, True)
        voxel_viz.lock_scale = (True, True, True)

        id = int(self.tile_name.split("_")[-1])
        planes = []
        for i in range(0, 8):
            planes = planes + self.add_voxel(id & (1 << i))

        for plane in planes:
            plane.parent = voxel_viz
            active_collection.objects.link(plane)

        return {'FINISHED'}

    def add_voxel(self, id):
        if id is 0:
            return []

        dx, dy, dz = 0.51, 0.51, 0.51
        x, y, z = 0.5, 0.5, 0.5

        if id == 0b0001:
            x, y, z = -x, -y, -z
        elif id == 0b0010:
            x, y, z = x, -y, -z
        elif id == 0b0100:
            x, y, z = -x,  y, -z
        elif id == 0b1000:
            x, y, z = x,  y, -z
        elif id == 0b0001_0000:
            x, y, z = -x, -y, z
        elif id == 0b0010_0000:
            x, y, z = x, -y, z
        elif id == 0b0100_0000:
            x, y, z = -x,  y, z
        elif id == 0b1000_0000:
            x, y, z = x,  y, z

        if x < 0.0:
            dx = -dx
        if y < 0.0:
            dy = -dy
        if z < 0.0:
            dz = -dz

        plane_x = self.add_plane((dx+x,    y,    z), axis=1)
        plane_y = self.add_plane((x, dy+y,    z), axis=0)
        plane_z = self.add_plane((x,    y, dz+z), axis=2)

        return [plane_z, plane_y, plane_x]

    def add_plane(self, location, axis):
        mesh_data = plane_mesh()
        plane = bpy.data.objects.new("plane", mesh_data)
        plane.hide_select = False
        plane.lock_rotation = (True, True, True)
        plane.lock_scale = (True, True, True)
        plane.location = location
        plane.scale = (0.4, 0.4, 0.4)
        if axis == 0:
            plane.rotation_euler = (3.14 / 2.0, 0.0, 0.0)
        elif axis == 1:
            plane.rotation_euler = (0.0, 3.14 / 2.0, 0.0)

        return plane

    def set_voxel_data(self, tile, location):
        tile.location = location
        tile.empty_display_size = 0.2
        tile.empty_display_type = 'PLAIN_AXES'
        tile.hide_render = True
        tile.show_bounds = False
        tile.lock_rotation = (True, True, True)
        tile.lock_scale = (True, True, True)


def menu_func(self, context):
    self.layout.operator(AddTileset.bl_idname, icon='VERTEXSEL')


def register():
    bpy.utils.register_class(ToggleVoxelVisualization)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ToggleVoxelVisualization)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
