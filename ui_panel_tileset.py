import bpy


class TylerPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Tyler"
    bl_idname = "OBJECT_PT_tyler"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = 'Tyler'

    @classmethod
    def poll(cls, context):
        active_object = bpy.context.active_object
        return active_object is not None and active_object.tileset_settings.is_tileset

    def draw(self, context):
        obj = bpy.context.active_object

        layout = self.layout

        row = layout.row()
        row.label(text="Tileset Selected: " + obj.name, icon='CUBE')

        if len(obj.children) == 0:
            row = layout.row()
            row.operator("tyler.create_tiles")
        else:
            row = layout.row()
            row.operator("tyler.toggle_voxels")
    

def register():
    bpy.utils.register_class(TylerPanel)


def unregister():
    bpy.utils.unregister_class(TylerPanel)


if __name__ == "__main__":
    register()
