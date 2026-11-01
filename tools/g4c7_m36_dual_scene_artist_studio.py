#!/usr/bin/env python3
"""M36: From rejected M35 native source build a DUAL-SCENE BLENDER ART AUTHORING MASTER.
Reference scene is untouched; editable counterpart has isolated mesh datablocks.
NO candidate geometry is generated. NO art, safety or construction approval.
"""
import bpy,hashlib,json,struct
from pathlib import Path
from mathutils import Vector

SOURCE=Path("artifacts/g4c7-m35-pinned-native-art-reject/M35_NATIVE_CITY_ART_HOLD.blend")
MANIFEST=Path("artifacts/g4c7-m35-pinned-native-art-reject/M35_MANIFEST.json")
OUT=Path("artifacts/g4c7-m36-artist-editable-studio")
OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads(MANIFEST.read_text())
assert m["art"]=="HOLD_NOT_ADOPTED" and m["formal_safety"]=="331_993_NOT_RUN"
assert sha(SOURCE)==m["blend"]["sha256"],"Refuse wrong M35 source"
bpy.ops.wm.open_mainfile(filepath=str(SOURCE.resolve()))
original=bpy.context.scene
original.name="M35_REJECTED_REFERENCE_LOCKED"
original["M36_ROLE"]="REJECTED_REFERENCE_DO_NOT_EDIT"
original["M36_SOURCE_SHA256"]=sha(SOURCE)
original_objects=list(original.objects)
original_meshes=[o for o in original_objects if o.type=="MESH"]
assert len(original_meshes)>=190,len(original_meshes)

def geometry_hash(objects):
    h=hashlib.sha256()
    for o in sorted((x for x in objects if x.type=="MESH"),key=lambda x:x.name):
        h.update(o.name.encode("utf-8"))
        for v in o.data.vertices:
            h.update(struct.pack("<ddd",*list(map(float,v.co))))
        for face in o.data.polygons:
            h.update(struct.pack("<I",len(face.vertices)))
            for idx in face.vertices:
                h.update(struct.pack("<I",idx))
        for row in o.matrix_world:
            h.update(struct.pack("<dddd",*list(map(float,row))))
    return h.hexdigest()
reference_hash=geometry_hash(original_meshes)
# New standalone scene; all editable mesh datablocks separately copied.
work=bpy.data.scenes.new("M36_AUTHORING_STUDIO_ART_HOLD")
work["M36_ROLE"]="MANUAL_AUTHORING_COPY_NO_ART_PASS"
work["M36_FORMAL_QA"]="NOT_RUN"
work["M36_MINECRAFT"]="FORBIDDEN"
work["M36_USER_ADOPTION"]=0
work["M36_SOURCE_REFERENCE_MESH_HASH"]=reference_hash
groups={}
for g in ("PUBLIC_AND_ROUTES","MAKER","HABITAT","RESEARCH","CULTURE",
          "URBAN_ENVELOPE","ART_REVIEW_CAMERAS","ART_BRIEF_GUIDES","LIGHTS"):
    col=bpy.data.collections.new("M36_"+g)
    work.collection.children.link(col)
    groups[g]=col
def group_for(o):
    n=o.name.upper()
    if o.type=="CAMERA":return "ART_REVIEW_CAMERAS"
    if o.type=="LIGHT":return "LIGHTS"
    if any(s in n for s in ("HAB","RESIDENT")):return "HABITAT"
    if "RESEARCH" in n:return "RESEARCH"
    if any(s in n for s in ("FAB","MAKER")):return "MAKER"
    if any(s in n for s in ("CULTURE","MARKET")):return "CULTURE"
    if any(s in n for s in ("CANOPY","ROOF","SKYLINE","COVER","SHELTER")):
        return "URBAN_ENVELOPE"
    return "PUBLIC_AND_ROUTES"
mapping={}
for source in original_objects:
    clone=source.copy()
    if source.data:clone.data=source.data.copy()
    clone.name="M36_EDIT_"+source.name
    groups[group_for(source)].objects.link(clone)
    clone["m36_source_object"]=source.name
    clone["m36_editable"]="YES"
    clone["m36_art_status"]="HOLD_UNREVIEWED"
    mapping[source.name]=clone
    if source.type=="MESH":
        assert clone.data.as_pointer()!=source.data.as_pointer()
        assert len(clone.data.vertices)==len(source.data.vertices)
        assert len(clone.data.polygons)==len(source.data.polygons)
assert len([o for o in work.objects if o.type=="MESH"])==len(original_meshes)
# Explicitly mark a tiny non-art edit on the editable-only copy; reference mesh untouched.
test_name="M35_FAB_ACTIVITY_ROOF"
src=bpy.data.objects[test_name]
test=mapping[test_name]
assert test.type=="MESH" and len(test.data.vertices)>0
old_co=tuple(test.data.vertices[0].co)
test.data.vertices[0].co.z+=.005
test.data.update()
test["m36_proof_edit_not_design"]="Z_PLUS_0_005_ABSTRACT_UNITS"
assert tuple(src.data.vertices[0].co)==old_co
assert abs(test.data.vertices[0].co.z-old_co[2]-.005)<1e-4
assert geometry_hash(original_meshes)==reference_hash

# NON-RENDERABLE, editable semantic goals for future direct sculpting.
# Anchors are NOT construction or verified route markers.
goals={
 "01_CIVIC_STREET_DENSITY":((-10,-8,1.8),"Every public approach sees a joined urban street, not 4 isolated camps"),
 "02_MAKER_REAL_STREET_DOOR":((-96,-30,1.8),"Unobstructed fully supported real fabrication access"),
 "03_RESEARCH_PUBLIC_EYE":((96,66,1.8),"Occupant sees functional research and urban life, not blank panels"),
 "04_HABITAT_LIVED_EYE":((-108,92,20),"Actual living rooms, garden, privacy and city panorama"),
 "05_CULTURE_REAL_EYE":((96,-81,2),"Original eye inside amphitheater tier: MUST RELOCATE/REWORK"),
 "06_STAIR_CONTINUITY":((-51,105,17),"Full body, landing and headroom not yet verified"),
 "07_NORTH_URBAN_COHESION":((0,240,60),"Distinctive inhabited city silhouette BOTH north and south"),
 "08_SOUTH_URBAN_COHESION":((0,-240,60),"No roof sheets, campus or giant blank walls")
}
for key,(loc,desc) in goals.items():
    ob=bpy.data.objects.new("M36_GOAL_"+key,None)
    groups["ART_BRIEF_GUIDES"].objects.link(ob)
    ob.empty_display_type="SPHERE";ob.empty_display_size=2.3
    ob.location=loc;ob.hide_render=True
    ob["m36_goal"]=desc
    ob["m36_evidence"]="NOT_PROVEN"
    ob["m36_type"]="ART_DIRECTION_NOT_GEOMETRY"
# A guide curve is editable, intentionally non-structural.
curve=bpy.data.curves.new("M36_URBAN_CONVIVIALITY_GUIDE","CURVE")
curve.dimensions="3D";curve.resolution_u=16;curve.bevel_depth=0
s=curve.splines.new("BEZIER");s.bezier_points.add(4)
for point,xyz in zip(s.bezier_points,[
 (-140,-90,1.8),(-30,-10,1.8),(24,10,1.8),(95,78,4),(-115,98,20)]):
    point.co=xyz;point.handle_left_type="AUTO";point.handle_right_type="AUTO"
guide=bpy.data.objects.new("M36_ARTIST_EDITABLE_EXPERIENCE_PATH_GUIDE",curve)
groups["ART_BRIEF_GUIDES"].objects.link(guide)
guide["route_safety"]="NOT_VERIFIED"
guide["guide_only"]="NOT_A_REAL_WALKABLE_FLOOR"
# Explicit camera bookmarks, same physical camera positions as original candidate.
camera_keys=[]
for name in ("SOUTH","NORTH","AERIAL","PUBLIC_EYE","FAB_EYE","RESEARCH_EYE","HAB_EYE","CULTURE_EYE","UPPER_BRIDGE_EYE"):
    original_cam="M35_CAMERA_"+name
    assert original_cam in mapping,original_cam
    camera_keys.append({"key":name,"source_camera":original_cam,"editable_camera":mapping[original_cam].name})
# Select SOUTH by default for visual baseline, not a flattering new camera trick.
work.camera=mapping["M35_CAMERA_SOUTH"]
work.render.engine="CYCLES";work.cycles.samples=12
work.render.resolution_x=760;work.render.resolution_y=456
work.render.resolution_percentage=100
work["M36_CAMERA_FIXED_SET"]=",".join(x["key"] for x in camera_keys)
work["M36_REFERENCE_IS_NOT_CITY_APPROVED"]=True
if bpy.context.window is not None:
    bpy.context.window.scene=work
dst=OUT/"M36_NATIVE_DUAL_SCENE_ARTIST_STUDIO.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(dst.resolve()))
# Independent check must reopen the saved file in a *fresh* Blender process.
res={
 "study":"M36_BLENDER_DIRECT_ARTIST_AUTHORING_STUDIO",
 "result":"METHOD_GATE_CANDIDATE_NEEDS_INDEPENDENT_NATIVE_REOPEN",
 "reference_original_sha256":sha(SOURCE),
 "reference_mesh_sha256":reference_hash,
 "locked_reference_scene":"M35_REJECTED_REFERENCE_LOCKED",
 "editable_scene":"M36_AUTHORING_STUDIO_ART_HOLD",
 "saved_blend":{"file":dst.name,"sha256":sha(dst)},
 "editable_mesh_count":len(original_meshes),
 "protected_reference_mesh_count":len(original_meshes),
 "separate_editable_datablocks":True,
 "deliberate_proof_edit":{"object":test_name,"vertex":0,"z_shift":.005,"reference_unchanged":True},
 "art_guide_count":len(goals),"fixed_camera_bookmarks":camera_keys,
 "whole_city_art":"HOLD_NOT_PASSED",
 "formal_331_993":"NOT_RUN","construction":"FORBIDDEN",
 "important":"Not a new city, no art pass, no safety pass, guide curves are not real geometry."}
(OUT/"M36_NATIVE_STUDIO_MANIFEST.json").write_text(json.dumps(res,indent=2,ensure_ascii=False))
print("M36_SAVED_DUAL_NATIVE_STUDIO_UNCHANGED_REFERENCED_SOURCE",dst,flush=True)
