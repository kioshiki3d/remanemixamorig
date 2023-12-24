import bpy
from bpy.types import Panel,Operator


bl_info = {
    "name": "rename_mixamorig_bonename", # 名前(自由記入)
    "author": "Kageji", # 作者(自由記入)
    "version": (0, 2), # バージョン(x,x,x)
    "blender": (2, 83, 0), # Blender Ver.(x,x,x)
    "location": "3D View > Sidebar", # ロケーション(自由記入)
    "description": "rename mixamorig bonename", # 詳細(自由記入)
    "warning": "", # ワーニング(自由記入)
    "support": "TESTING", # "OFFICAL"、"COMMUNITY"、"TESTING"
    "wiki_url": "", # URL(自由記入)
    "tracker_url": "", # URL(自由記入)
    "category": "Object", # カテゴリー(要検索)
}


class KJ_Rename_PT_Panel(Panel):
    bl_label = "Rename Mixamori"# 展開時のラベル名
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "KJaddon" # 横タブ名


    @classmethod
    def poll(cls, context):
        return bpy.context.active_object.type == "ARMATURE"


    def draw(self, context):
        layout = self.layout
        # Eyedropper要検討
        #scene = context.scene
        #layout.prop(scene, "target", text="", icon='ARMATURE_DATA') 
        #layout.separator()
        layout.label(text="rename mixamorig")
        layout.operator(KJ_rename_bone.bl_idname, text="rename")
        layout.separator()
        layout.label(text="dissolve upperchest")
        layout.operator(KJ_dissolve_chest.bl_idname, text="dissolve")


class KJ_rename_bone_base(Operator):
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


class KJ_rename_bone(KJ_rename_bone_base):
    bl_idname = "kjrename.operator"
    bl_label = "KJ_rename_bone"


    def execute(self, context):
        super().execute(context)
        return {"FINISHED"}


class KJ_dissolve_chest(KJ_rename_bone_base):
    bl_idname = "kjdissolve.operator"
    bl_label = "KJ_dissolve_chest"


    def execute(self, context):
        super().execute(context)
        obj = bpy.context.active_object
        for bone in obj.data.bones:
            bonename = bone.name

            if "UpperChest" in bonename:
                bpy.ops.armature.dissolve()
            if "LowerChest" in bonename:
                bonename = bonename.replace("Lower", "")
                bone.name = bonename + "_R" 
            
        return {"FINISHED"}


classes = [KJ_Rename_PT_Panel, KJ_rename_bone, KJ_dissolve_chest]


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
