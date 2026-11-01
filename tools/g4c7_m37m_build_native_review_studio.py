#!/usr/bin/env python3
"""M37-M build review workspace from immutable M37-L rejected native file.
No city candidate is generated; review UI source is embedded for user activation.
"""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=Path("artifacts/g4c7-m37l-verified-native-city-master-art-hold")
OUT=Path("artifacts/g4c7-m37m-review-studio-CI")
OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,"tools")
import g4c7_m37m_blender_review_panel as ui
source=ROOT/"M37L_SINGLE_CITY_AUTHOR_MASTER_ART_HOLD.blend"
pin=json.loads((ROOT/"M37L_NATIVE_MASTER_MANIFEST.json").read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(source)==pin["native_blend"]["sha256"]
assert pin["art"]=="HOLD_UNREVIEWED" and pin["minecraft"]=="FORBIDDEN"
bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
old=bpy.data.scenes[ui.BASE]
assert len([o for o in old.objects if o.type=="MESH"])==199
assert old.get("M37L_MINECRAFT")=="FORBIDDEN"
studio=bpy.data.scenes.new(ui.WORK)
studio.world=old.world
studio.render.engine="CYCLES"
studio.cycles.samples=1
studio.cycles.max_bounces=2
studio.render.resolution_x=480
studio.render.resolution_y=300
studio.render.resolution_percentage=100
studio.render.image_settings.file_format="PNG"
col=bpy.data.collections.new("M37M_EDITABLE_REJECTED_SOURCE_COPY")
studio.collection.children.link(col)
copies={}
for obj in old.objects:
    new_obj=obj.copy()
    if obj.data:new_obj.data=obj.data.copy()
    new_obj.name=ui.PREFIX+obj.name
    new_obj["M37M_ROLE"]="REVIEW_ONLY_EDIT_COPY_NOT_ART_ADOPTED"
    col.objects.link(new_obj)
    copies[obj.name]=new_obj
for old_obj in old.objects:
    if old_obj.parent:copies[old_obj.name].parent=copies[old_obj.parent.name]
for key,value in ui.CHARTER.items():studio[key]=value
studio["M37M_BASE_SHA256"]=sha(source)
studio["M37M_PREVIEW_ACTIVE"]=False
studio["M37M_PREVIEW_ISSUE"]=""
studio["M37M_PREVIEW_DELTA"]=0.0
studio["M37M_NATIVE_SCULPTING"]="NOT_PERFORMED_EDITOR_READY_ONLY"
studio["M37M_STUDIO_PURPOSE"]="REVIEW_9_CAMERAS_SELECT_REAL_MESHES_BOUNDED_GEOMETRY_EDIT_ROLLBACK"
text=bpy.data.texts.new("M37M_RUN_ONCE_TO_ENABLE_REVIEW_PANEL.py")
text.write(Path("tools/g4c7_m37m_blender_review_panel.py").read_text())
other=bpy.data.texts.new("M37M_ORIGINAL_ART_FAILINGS_JA.txt")
other.write("M37-L ART REJECT. 9固定視点で遠景・公共・製造・研究・居住・高所を照合。"
            "単純な曲面チューブの外形、巨大壁、活動と住居が見えないこと、"
            "用途室の入り口からの実通行未検証、MakeCode未変換。"
            "このレビュー道具の2メッシュ移動は技術デモであり、"
            "実建築の連続性、安全性、ART採用を意味しない。")
studio.camera=copies["M37L_CAMERA_RESEARCH_EYE"]
ui.register()
ui.validate_scene()
# Validate preview/edit/revert against REAL Blender vertex data before saving.
test=ui.apply_preview("RESEARCH",.6)
assert len(test["changed_meshes"])==2
assert ui.revert_preview()["changed"]==[]
# Negative controls must FAIL CLOSED, even when a preview is active.
bad=[]
def reject(name,fn):
    try:fn()
    except (AssertionError,ValueError,KeyError):bad.append(name);return
    raise AssertionError("FAIL_OPEN:"+name)
reject("unrecognized_issue",lambda:ui.apply_preview("OTHER",.5))
reject("unbounded_delta",lambda:ui.apply_preview("RESEARCH",4.0))
reject("false_art_promotion",lambda: studio.__setitem__("M37M_ART","PASS") or ui.validate_scene())
studio["M37M_ART"]=ui.CHARTER["M37M_ART"]
# A mutated unrelated mesh must be detected even while main target is OK.
rogue=next(o for o in studio.objects if o.type=="MESH" and
    o.name!=ui.PREFIX+"M37L_RESEARCH_RESEARCH_ACTUAL_ROOM_FLOOR")
rogue.data.vertices[0].co.z+=1.0;rogue.data.update()
reject("out_of_scope_mesh_edit",ui.validate_scene)
src_obj=old.objects[rogue.name[len(ui.PREFIX):]]
rogue.data.vertices[0].co=src_obj.data.vertices[0].co.copy();rogue.data.update()
ui.validate_scene()
ui.apply_preview("RESEARCH",.5)
reject("double_preview",lambda:ui.apply_preview("RESEARCH",.5))
ui.revert_preview()
reject("double_rollback",ui.revert_preview)
assert len(bad)==6,bad
studio["M37M_TEST_NEGATIVES"]=json.dumps(bad)
# Author-review camera is paired to actual unchanged source fixed viewpoints.
views=("AERIAL","MAKER_EYE","RESEARCH_EYE","HABITAT_EYE")
photos={}
for key in views:
    cam=copies["M37L_CAMERA_"+key]
    studio.camera=cam
    studio.render.filepath=str((OUT/("M37M_REFERENCE_"+key+".png")).resolve())
    bpy.ops.render.render(write_still=True,scene=studio.name)
    img=Path(studio.render.filepath)
    assert img.stat().st_size>1500
    photos[key]={"file":img.name,"sha256":sha(img)}
    print("M37M_REFERENCE_RENDER",key,flush=True)
# Save only a zero-trial state, with source and copy in separate scenes.
studio.camera=copies["M37L_CAMERA_RESEARCH_EYE"]
assert not studio["M37M_PREVIEW_ACTIVE"]
ui.validate_scene()
target=OUT/"M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(target.resolve()))
manifest={
 "schema":"g4c7-m37m-direct-authoring-review-studio-v1",
 "status":"METHOD_STUDIO_ONLY_ART_REJECT_SOURCE",
 "source_blend":{"name":source.name,"sha256":sha(source)},
 "native_blend":{"name":target.name,"sha256":sha(target),"bytes":target.stat().st_size},
 "old_source_scene":ui.BASE,"editable_copy_scene":ui.WORK,
 "unchanged_original_meshes":199,"editable_copy_meshes":199,
 "fixed_camera_copies":9,"issue_targets":ui.ISSUES,
 "actual_test":"two real native mesh datablocks moved and rolled back",
 "negative_controls_rejected":bad,"review_renders":photos,
 "not_proven":{"room_route":"NOT_RUN","art":"REJECT_UNCHANGED",
               "formal_331_993":"NOT_RUN","Minecraft":"FORBIDDEN",
               "full_sculptor_workflow":"NOT_HAND_GUI_TESTED"},
 "official_adoption":0}
(OUT/"M37M_REVIEW_STUDIO_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print("M37M_STUDIO_SAVED",json.dumps({"size":target.stat().st_size,"hash":sha(target),"negative":bad}),flush=True)
