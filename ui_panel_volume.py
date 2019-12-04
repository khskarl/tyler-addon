import bpy


class TylerVolumePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Tyler"
    bl_idname = "OBJECT_PT_tyler_volume"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = 'Tyler'

    @classmethod
    def poll(cls, context):
        active_object = bpy.context.active_object
        return active_object is not None and active_object.volume_settings.is_volume

    def draw(self, context):
        obj = bpy.context.active_object

        layout = self.layout

        row = layout.row()
        row.label(text="Volume Selected: " + obj.name, icon='UV_DATA')

#		row = layout.row()
#		row.operator("tyler.toggle_voxels")
#


def has_tiles(tileset):
    return len(tileset.children) > 0


def register():
    bpy.utils.register_class(TylerVolumePanel)


def unregister():
    bpy.utils.unregister_class(TylerVolumePanel)


if __name__ == "__main__":
    register()
