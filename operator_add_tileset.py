import bpy

from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
)


class TilesetSettings(bpy.types.PropertyGroup):
    is_tileset: bpy.props.BoolProperty()
    tile_size: bpy.props.IntProperty()


class AddTileset(bpy.types.Operator):
    """Add an empty tileset"""
    bl_idname = "tyler.add_tileset"
    bl_label = "Add Tileset"
    bl_options = {'REGISTER', 'UNDO'}

    location: FloatVectorProperty(
        name="Location",
        subtype='TRANSLATION',
    )

    @classmethod
    def poll(cls, context):
        return context.view_layer.active_layer_collection.collection is not None

    def execute(self, context):
        active_collection = context.view_layer.active_layer_collection.collection

        obj = bpy.data.objects.new("Tileset", None)

        active_collection.objects.link(obj)

        obj.location = self.location
        obj.empty_display_size = 1.0
        obj.empty_display_type = 'ARROWS'
        obj.hide_render = True
        obj.show_bounds = True
        obj.lock_rotation = (True, True, True)
        obj.lock_scale = (True, True, True)

        obj.tileset_settings.is_tileset = True
        obj.tileset_settings.tile_size = 2

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddTileset.bl_idname, icon='MESH_CUBE')


def register():
    bpy.utils.register_class(TilesetSettings)
    bpy.types.Object.tileset_settings = bpy.props.PointerProperty(
        type=TilesetSettings)
    bpy.utils.register_class(AddTileset)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(TilesetSettings)
    bpy.utils.unregister_class(AddTileset)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
