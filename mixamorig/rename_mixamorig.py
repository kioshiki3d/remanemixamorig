import bpy
from bpy.types import Panel,Operator

bl_info = {
    "name": "rename_mixamorig_bonename",
    "author": "Kageji",
    "version": (0, 1),
    "blender": (2, 83, 0),
    "location": "3D View > Sidebar",
    "description": "rename mixamorig bonename",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

class KJ_Rename_PT_Panel(Panel):
    bl_label = "Rename Mixamori"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "KJaddon"

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object.type == "ARMATURE"

    def draw(self, context):
        layout = self.layout
        layout.label(text="rename mixamorig")
        layout.operator(KJ_rename_bone.bl_idname, text="rename")

class KJ_rename_bone(Operator):
    bl_idname = "kjrename.operator"
    bl_label = "KJ_rename_bone"

    def execute(self, context):
        obj = bpy.context.active_object
        for bone in obj.data.bones:
            bonename = bone.name

            try:
                bonename = bonename.replace("mixamorig:", "")
                bone.name = bonename
            except:
                pass

            try:
                bonename = bonename.replace("Spine1", "LowerChest")
                bone.name = bonename
            except:
                pass
            try:
                bonename = bonename.replace("Spine2", "UpperChest")
                bone.name = bonename
            except:
                pass

            if "Right" in bonename:
                bonename = bonename.replace("Right", "")
                bone.name = bonename + "_R" 
            elif "Left" in bonename:
                bonename = bonename.replace("Left", "")
                bone.name = bonename + "_L" 
        return {"FINISHED"}


classes = [KJ_Rename_PT_Panel,KJ_rename_bone]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("rename mixamorig bone name is active")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("rename mixamorig bone name is inactive")

if __name__ == "__main__":
    register()