import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper

from bpy.props import (
    PointerProperty,
    StringProperty,
    BoolProperty,
)


class ToggleVoxels(bpy.types.Operator):
    """Toggle voxels visualization for a tileset"""
    bl_idname = "tyler.toggle_voxels"
    bl_label = "Toggle Voxels Visualization"
    bl_options = {'REGISTER', 'UNDO'}

    is_visible: BoolProperty(
        name="Is Visible"
    )

    def execute(self, context):
        tileset = context.object

        for child in tileset.children:
            bpy.ops.tyler.toggle_voxel_visualization(tile_name=child.name, is_visible=self.is_visible)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddTileset.bl_idname, icon='VERTEXSEL')


def register():
    bpy.utils.register_class(ToggleVoxels)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ToggleVoxels)


if __name__ == "__main__":
    register()
