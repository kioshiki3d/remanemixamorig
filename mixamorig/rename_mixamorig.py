import re
import bpy
from bpy.types import Panel,Operator

bl_info = {
    "name": "rename_mixamorig_bonename", # 名前(自由記入)
    "author": "Kageji", # 作者(自由記入)
    "version": (1, 1), # バージョン(x,x,x)
    "blender": (2, 83, 0), # Blender Ver.(x,x,x)
    "location": "3D View > Sidebar", # ロケーション(自由記入)
    "description": "rename mixamorig bonename", # 詳細(自由記入)
    "warning": "", # ワーニング(自由記入)
    "support": "COMMUNITY", # "OFFICAL"、"COMMUNITY"、"TESTING"
    "wiki_url": "https://github.com/kioshiki3d/remanemixamorig", # URL(自由記入)
    "tracker_url": "https://twitter.com/shadow003min", # URL(自由記入)
    "category": "Object", # カテゴリー(要検索)
}

class KJ_Rename_PT_Panel(Panel):
    bl_label = "Rename Mixamorig"# 展開時のラベル名
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RenameRig" # 横タブ名

    # @classmethod
    # def poll(cls, context):
        # return bpy.context.active_object.type == "ARMATURE"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop_search(scene, "targetArmature", bpy.data, "armatures", text="", icon="ARMATURE_DATA")
        layout.separator()
        layout.label(text="rename mixamorig")
        layout.operator(KJ_rename_bone.bl_idname, text="rename")
        layout.separator()
        layout.label(text="dissolve upperchest")
        layout.operator(KJ_dissolve_chest.bl_idname, text="dissolve")


class KJ_rename_bone_base(Operator):
    obj = None
    rpt_txt = ""

    def renameRL(self, name, target):
        new_name = name
        name_end = ""
        symbol = "_" + target[0].upper()
        if (new_name[-4:-3]==".") and (new_name[-3:].isnumeric()):
            name_end = new_name[-4:]
            new_name = new_name[:-4]
        new_name = re.sub("[.]"+target, symbol, new_name, flags=re.IGNORECASE)
        new_name = re.sub("_"+target, symbol, new_name, flags=re.IGNORECASE)
        if target.lower() in new_name.lower():
            new_name = re.sub(target+"[.]", "", new_name, flags=re.IGNORECASE)
            new_name = re.sub(target+"_", "", new_name, flags=re.IGNORECASE)
            new_name = re.sub(target, "", new_name, flags=re.IGNORECASE)
            new_name = new_name + symbol
        new_name = new_name + name_end
        return new_name


    def execute(self, context):
        if context.scene.targetArmature==None:
            self.rpt_txt = "select armature"
            return {"FINISHED"}

        if context.object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode = "OBJECT")

        obj_name = context.scene.targetArmature.name
        self.obj = bpy.data.objects[obj_name] #bpy.context.active_object
        for bone in self.obj.data.bones:
            bonename = bone.name
            bonename = bonename.replace("mixamorig:", "")
            bonename = bonename.replace("Spine1", "LowerChest")
            bonename = bonename.replace("Spine2", "UpperChest")
            bonename = self.renameRL(bonename, "Right")
            bonename = self.renameRL(bonename, "left")
            bone.name = bonename
        return {"FINISHED"}


class KJ_rename_bone(KJ_rename_bone_base):
    bl_idname = "kjrename.operator"
    bl_label = "KJ_rename_bone"

    def execute(self, context):
        super().execute(context)
        if self.rpt_txt=="":
            self.rpt_txt = "FINISHED rename mixamo rig name"
        self.report({'INFO'}, self.rpt_txt)
        return {"FINISHED"}


class KJ_dissolve_chest(KJ_rename_bone_base):
    bl_idname = "kjdissolve.operator"
    bl_label = "KJ_dissolve_chest"

    def execute(self, context):
        super().execute(context)
        if self.rpt_txt!="":
            self.report({'INFO'}, self.rpt_txt)
            return {"FINISHED"}

        context.view_layer.objects.active = self.obj
        bpy.ops.object.mode_set(mode = "EDIT")
        for bone in self.obj.data.edit_bones:
            bonename = bone.name
            if "LowerChest" in bonename:
                lowerchest_bone = bone
            if "UpperChest" in bonename:
                upperchest_bone = bone
        
        upper_name = upperchest_bone.name
        chestname = lowerchest_bone.name
        chestname = chestname.replace("Lower", "")
        upper_tail = upperchest_bone.tail
        lowerchest_bone.tail = upper_tail
        self.obj.data.edit_bones.remove(upperchest_bone)
        lowerchest_bone.name = chestname
        bpy.ops.object.mode_set(mode = "OBJECT")

        for child in self.obj.children:
            if isinstance(child.data, bpy.types.Mesh):
                # UpperChestのウエイトがない場合
                if not child.vertex_groups.get(upper_name):
                    continue
                # UpperありLowerなしの場合
                if not child.vertex_groups.get(chestname):
                    child.vertex_groups[upper_name].name = chestname
                    continue
                # 両方ありの場合
                for id, vert in enumerate(child.data.vertices):
                    groups = [v.group for v in vert.groups]
                    lower_weight = 0
                    upper_weight = 0
                    if child.vertex_groups[chestname].index in groups:
                        lower_weight = child.vertex_groups[chestname].weight(id)
                    if child.vertex_groups[upper_name].index in groups:
                        upper_weight = child.vertex_groups[upper_name].weight(id)
                    weight = lower_weight + upper_weight
                    if weight > 0:
                        child.vertex_groups[chestname].add([id], weight ,"REPLACE")
                child.vertex_groups.remove(child.vertex_groups[upper_name])
        self.report({'INFO'}, "FINISHED rename mixamo rig name and dissolve upperchest")
        return {"FINISHED"}


classes = [KJ_Rename_PT_Panel, KJ_rename_bone, KJ_dissolve_chest]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.targetArmature = bpy.props.PointerProperty(type=bpy.types.Object) # StringProperty() #
    print("rename mixamorig bone name is active")


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.targetArmature
    print("rename mixamorig bone name is inactive")


if __name__ == "__main__":
    register()
