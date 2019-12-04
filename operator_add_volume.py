import bpy

from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
)


class VolumeSettings(bpy.types.PropertyGroup):
    is_volume: bpy.props.BoolProperty()
    size: bpy.props.FloatVectorProperty()


class AddVolume(bpy.types.Operator):
    """Add an empty voxel volume"""
    bl_idname = "tyler.add_volume"
    bl_label = "Add Voxel Volume"
    bl_options = {'REGISTER', 'UNDO'}

    location: FloatVectorProperty(
        name="Location",
        subtype='TRANSLATION',
    )

    size: FloatVectorProperty(
        name="Size",
        subtype='TRANSLATION',
    )

    @classmethod
    def poll(cls, context):
        return context.view_layer.active_layer_collection.collection is not None

    def execute(self, context):
        active_collection = context.view_layer.active_layer_collection.collection

        obj = bpy.data.objects.new("VoxelVolume", None)

        active_collection.objects.link(obj)

        obj.location = self.location
        obj.empty_display_size = 1.0
        obj.empty_display_type = 'ARROWS'
        obj.hide_render = True
        obj.show_bounds = True
        obj.lock_rotation = (True, True, True)
        obj.lock_scale = (True, True, True)

        obj.volume_settings.is_volume = True
        obj.volume_settings.size = self.size

        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddTileset.bl_idname, icon='UV_VERTEXSEL')


def register():
    bpy.utils.register_class(VolumeSettings)
    bpy.types.Object.volume_settings = bpy.props.PointerProperty(
        type=VolumeSettings)
    bpy.utils.register_class(AddVolume)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(VolumeSettings)
    bpy.utils.unregister_class(AddTileset)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()
