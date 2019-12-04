import bpy
import mathutils
import math
tile_math = bpy.data.texts['tile_math.py'].as_module()

from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
)


class CreateTiles(bpy.types.Operator):
    """Create all the tile combinations of a tileset"""
    bl_idname = "tyler.create_tiles"
    bl_label = "Create Tiles"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        ids = tile_math.unique_tile_ids()
        WIDTH = 10.0
        for i, id in enumerate(ids):
            tile = self.new_tile(id, context)
            x = (i % WIDTH) * 4.0  + 1.0
            y = int(i / WIDTH) * 4.0 + 1.0
            z = 1.0
            self.set_tile_data(tile, (x, y, z))
        return {'FINISHED'}

    def new_tile(self, id, context):
        active_collection = context.view_layer.active_layer_collection.collection

        tile = bpy.data.objects.new("tile_" + str(id), None)
        active_collection.objects.link(tile)

        tileset = context.active_object
        tile.parent = tileset
        return tile

    def set_tile_data(self, tile, location):
        tile.location = location
        tile.empty_display_size = 1.0
        tile.empty_display_type = 'CUBE'
        tile.hide_render = True
        tile.show_bounds = True
        tile.lock_rotation = (True, True, True)
        tile.lock_scale = (True, True, True)


def menu_func(self, context):
    self.layout.operator(AddTileset.bl_idname, icon='MESH_CUBE')


def register():
    bpy.utils.register_class(CreateTiles)


def unregister():
    bpy.utils.unregister_class(CreateTiles)


if __name__ == "__main__":
    register()
