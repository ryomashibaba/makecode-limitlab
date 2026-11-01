#!/usr/bin/env python3
"""M37-C: in-place native Blender topology surgery in M36 editable scene only.
Method proof, not a city, art approval, safety approval, or Minecraft construction.
"""
import bpy, hashlib, json, math
from pathlib import Path

BASE=Path("artifacts/g4c7-m36-verified-native-author-studio")
SOURCE=BASE/"M36_NATIVE_DUAL_SCENE_ARTIST_STUDIO.blend"
SOURCE_MANIFEST=BASE/"M36_NATIVE_STUDIO_MANIFEST.json"
OUT=Path("artifacts/g4c7-m37c-native-build")
OUT.mkdir(parents=True,exist_ok=True)
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

old=json.loads(SOURCE_MANIFEST.read_text(encoding="utf8"))
assert sha(SOURCE)==old["saved_blend"]["sha256"]
assert old["whole_city_art"]=="HOLD_NOT_PASSED"
assert old["formal_331_993"]=="NOT_RUN"
assert old["construction"]=="FORBIDDEN"
bpy.ops.wm.open_mainfile(filepath=str(SOURCE.resolve()))
ref=bpy.data.scenes["M35_REJECTED_REFERENCE_LOCKED"]
edit=bpy.data.scenes["M36_AUTHORING_STUDIO_ART_HOLD"]
assert len([o for o in ref.objects if o.type=="MESH"])==208
assert len([o for o in edit.objects if o.type=="MESH"])==208
assert edit.get("M36_MINECRAFT")=="FORBIDDEN"

# A single open-to-sky public corridor carved through formerly continuous
# culture platforms. This edits the *existing* mesh datablocks (not just
# adding or overlaying another proxy box). Continuous ground floor is retained.
# It is intentionally a LOCAL NATIVE TOPOLOGY METHOD PROOF, not urban art.
target_names=[
 "M35_CULTURE_STAGE",
 "M35_CULTURE_OCCUPIED_TIER_0",
 "M35_CULTURE_OCCUPIED_TIER_1",
 "M35_CULTURE_OCCUPIED_TIER_2",
 "M35_CULTURE_OCCUPIED_TIER_3",
]
world_left,world_right=88.5,103.5
edited={}
def add_prism(v,f,x0,x1,y0,y1,z0,z1):
    k=len(v)
    v.extend([(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
              (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)])
    f.extend([tuple(k+i for i in face) for face in (
        (3,2,1,0),(4,5,6,7),(0,1,5,4),
        (1,2,6,5),(2,3,7,6),(3,0,4,7))])
for name in target_names:
    source=ref.objects[name]
    obj=edit.objects["M36_EDIT_"+name]
    assert obj.get("m36_source_object")==name
    assert obj.type==source.type=="MESH"
    assert obj.data.as_pointer()!=source.data.as_pointer()
    assert len(source.data.vertices)==8 and len(source.data.polygons)==6,(name,len(source.data.vertices),len(source.data.polygons))
    assert not obj.parent and all(abs(float(v))<1e-6 for v in obj.rotation_euler)
    assert all(abs(float(v)-1)<1e-6 for v in obj.scale)
    xs=[v.co.x for v in obj.data.vertices]
    ys=[v.co.y for v in obj.data.vertices]
    zs=[v.co.z for v in obj.data.vertices]
    lo,hi=min(xs),max(xs)
    left=world_left-obj.location.x
    right=world_right-obj.location.x
    assert lo+5<left<right<hi-5,(name,lo,left,right,hi)
    v,f=[],[]
    add_prism(v,f,lo,left,min(ys),max(ys),min(zs),max(zs))
    add_prism(v,f,right,hi,min(ys),max(ys),min(zs),max(zs))
    obj.data.clear_geometry()
    obj.data.from_pydata(v,[],f)
    obj.data.update()
    assert len(obj.data.vertices)==16 and len(obj.data.polygons)==12
    assert all(obj.location.x+q.co.x <= world_left+1e-5 or
               obj.location.x+q.co.x >= world_right-1e-5
               for q in obj.data.vertices)
    obj["M37C_TOPOLOGY_METHOD"]="IN_PLACE_SPLIT_EXISTING_PLATFORM_BY_OPEN_CORRIDOR"
    obj["M37C_ART"]="NOT_REVIEWED"
    edited[name]={"before_verts":len(source.data.vertices),
                  "after_verts":len(obj.data.vertices),
                  "before_faces":len(source.data.polygons),
                  "after_faces":len(obj.data.polygons),
                  "removed_world_x":[world_left,world_right],
                  "y_range":[round(float(min(ys)+obj.location.y),4),
                             round(float(max(ys)+obj.location.y),4)]}

# Preserve exact source reference: no scene references or geometry in ref are edited.
assert all(o.name.startswith("M35_") for o in ref.objects)
assert len([o for o in edit.objects if o.type=="MESH"])==208
edit["M37C_KIND"]="NATIVE_EXISTING_MESH_TOPOLOGY_METHOD_PROOF"
edit["M37C_ART_STATUS"]="ART_HOLD_NO_QUALITY_CLAIM"
edit["M37C_FORMAL_QA"]="NOT_RUN"
edit["M37C_MINECRAFT"]="FORBIDDEN"
edit["M37C_USER_ADOPTION"]=0
edit["M37C_REFERENCE_LOCK"]="M35_REJECTED_REFERENCE_LOCKED"
edit["M37C_OLD_SOURCE_SHA256"]=sha(SOURCE)
# Demonstrated support footprint only; no claimed swept-body certification.
floor=edit.objects["M36_EDIT_M35_CULTURE_GROUND"]
min_x,max_x=(min(v.co.x for v in floor.data.vertices)+floor.location.x,
             max(v.co.x for v in floor.data.vertices)+floor.location.x)
min_y,max_y=(min(v.co.y for v in floor.data.vertices)+floor.location.y,
             max(v.co.y for v in floor.data.vertices)+floor.location.y)
assert min_x < world_left < 96 < world_right < max_x
assert min_y < -124 < -30 < max_y
# This local footprint is not a G0/S1/etc assessment.
edit["M37C_ROUTE_FOOTPRINT_ONLY"]="CULTURE_GROUND x96 y[-124,-30] floor footprint; clearance NOT certified"
if bpy.context.window:
    bpy.context.window.scene=edit
edit.camera=edit.objects["M36_EDIT_M35_CAMERA_SOUTH"]
edit.render.engine="CYCLES"
edit.cycles.samples=6
edit.render.resolution_x=640
edit.render.resolution_y=384
edit.render.resolution_percentage=100
edit.render.image_settings.file_format="PNG"
saved=OUT/"M37C_NATIVE_DIRECT_TOPOLOGY_EDIT_ART_HOLD.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(saved.resolve()))
images={}
for camera_key in ("SOUTH","AERIAL","PUBLIC_EYE","CULTURE_EYE"):
    cam=edit.objects["M36_EDIT_M35_CAMERA_"+camera_key]
    edit.camera=cam
    path=OUT/("M37C_"+camera_key+".png")
    edit.render.filepath=str(path.resolve())
    bpy.ops.render.render(write_still=True,scene=edit.name)
    assert path.exists() and path.stat().st_size>2000
    images[camera_key]={"file":path.name,"sha256":sha(path)}
    print("M37C_FIXED_CAMERA_IMAGE",camera_key,flush=True)

# Native BLEND was saved *before* temporarily switching cameras for renders.
m={
 "study":"M37C_NATIVE_IN_PLACE_MESH_SURGERY_NOT_ARTWORK",
 "source_blend_sha256":sha(SOURCE),
 "saved_blend":{"file":saved.name,"sha256":sha(saved),"bytes":saved.stat().st_size},
 "reference_scene":"M35_REJECTED_REFERENCE_LOCKED",
 "edited_scene":"M36_AUTHORING_STUDIO_ART_HOLD",
 "all_editable_meshes":208,
 "all_reference_meshes":208,
 "actual_modified_meshes":edited,
 "fixed_camera_renderings":images,
 "original_fixed_cameras_retained":9,
 "art":"HOLD_NOT_ADOPTED",
 "original_M35_art":"REJECT",
 "formal_331_993":"NOT_RUN",
 "gates_G0_S1_G1_G2_G3":"NOT_RUN",
 "continuous_full_body_sweep":"NOT_RUN",
 "structure":"NOT_CERTIFIED",
 "minecraft":"FORBIDDEN",
 "scope":"5 existing culture meshes directly edited; no added buildings; no broad city art improvement claim"
}
(OUT/"M37C_NATIVE_AUTHOR_MANIFEST.json").write_text(
 json.dumps(m,ensure_ascii=False,indent=2),encoding="utf8")
print("M37C_SAVED_NATIVE_METHOD_PROOF",json.dumps(
 {"blend_sha256":sha(saved),"modified":list(edited),"renders":list(images)},
 ensure_ascii=False),flush=True)
