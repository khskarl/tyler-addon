import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper
from mathutils import *
from math import *
from bpy.props import (
    FloatVectorProperty,
)

class CubeMarching(bpy.types.Operator):
    """Cube march voxel volume using a tileset"""
    bl_idname = "tyler.cube_marching"
    bl_label = "Cube March Volume"
    bl_options = {'REGISTER', 'UNDO'}

    extends: FloatVectorProperty(
        name="Extends",
        default=(4.0, 4.0, 3.0)
    )

    def execute(self, context):
        volume_obj = context.object

        volume = self.voxelize(volume_obj)
        march_positions = self.get_march_positions()
#        print(volume)
        print(march_positions)
        ids = get_ids(march_positions, volume)
    
        print(ids)
        return {'FINISHED'}
    
    def get_march_positions(self):
        dx = 1.0
        positions = []
        curr_pos = Vector((0.0, 0.0, 0.0))
        while curr_pos.x + dx < self.extends[0]:
            curr_pos.x += dx
            while curr_pos.y + dx < self.extends[1]:
                curr_pos.y += dx
                while curr_pos.z + dx < self.extends[2]:
                    curr_pos.z += dx
                    positions.append(curr_pos.copy())
                curr_pos.z = 0.0
            curr_pos.y = 0.0
        return positions
    
    def voxelize(self, obj):
        voxel_list = []
        for child in obj.children:
            loc = child.matrix_local.translation
            voxel_list.append(loc)

        volume = []
        for i in range(0, int(self.extends[0])):
            depth_list = []
            for j in range(0, int(self.extends[1])):
                height_list = []
                for k in range(0, int(self.extends[2])):
                    height_list.append(0)
                depth_list.append(height_list)
            volume.append(depth_list)
                
            
        for voxel in voxel_list:
            x = floor(voxel.x)
            y = floor(voxel.y)
            z = floor(voxel.z)
            if x > self.extends[0] or y > self.extends[1] or z > self.extends[2]:
                continue
             
            volume[x][y][z] = 1
        
        return volume
    
def get_ids(positions, volume):
    ids = []
    for pos in positions:
        id = get_id(pos, volume)
        ids.append(id)
    return ids

def get_id(center, volume):
    dx = 0.4
    pos = [Vector((0.0, 0.0, 0.0)) for i in range(0, 8)]
    pos[0] = center + Vector((-dx, -dx, -dx))
    pos[1] = center + Vector(( dx, -dx, -dx))
    pos[2] = center + Vector((-dx,  dx, -dx))
    pos[3] = center + Vector(( dx,  dx, -dx))
    pos[4] = center + Vector((-dx, -dx,  dx))
    pos[5] = center + Vector(( dx, -dx,  dx))
    pos[6] = center + Vector((-dx,  dx,  dx))
    pos[7] = center + Vector(( dx,  dx,  dx))
    
    indices = [[floor(p.x), floor(p.y), floor(p.z)] for p in pos]
    
    
    bit = [0 for i in range(0, 8)]
    for i in range(0, 8):
        (x, y, z) = indices[i]
        bit[i] = volume[x][y][z]
        
    id = 0
    for i in range(0, 8):
        id = id | (bit[i] << i)
        
    return id
        
    
    
    

def menu_func(self, context):
    self.layout.operator(CubeMarching.bl_idname, icon='VERTEXSEL')


def register():
    bpy.utils.register_class(CubeMarching)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(CubeMarching)


if __name__ == "__main__":
    register()
