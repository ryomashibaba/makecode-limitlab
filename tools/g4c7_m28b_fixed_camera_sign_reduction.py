#!/usr/bin/env python3
"""M28B: direct two-camera image-driven correction to oversize sign and
threshold-occluding bench in M28 REAL native blend. Preserve all other meshes.
ART HOLD; no Minecraft/QA claims.
"""
from pathlib import Path
import json,hashlib,os,sys
SEED=Path("artifacts/m28b_pinned_m28")
OUT=Path("artifacts/g4c7-m28b-gallery-sign-occlusion-correction")/("run_"+os.getenv("GITHUB_SHA","local")[:12])
PIN="87c723409c61eea8bd6cacbda021394c208d0ee28257f978d3c7bfcc1b2399c2"
GLB_PIN="014fb48a151d87e25cb826893f15aeee254bd5f80093f31349882bf09713c0e0"
ORIGIN=(-43.,37.,9.6)
SIGN="M28_CINEMATIC_WELCOME_SIGN"
HEAD="M28_CENTRAL_SIGN_HEAD"
SUB="M28_CENTRAL_SIGN_SUB"
HIDE=("M28_VIEWING_SEAT_WARM_LOW_BENCH",
 "M28_VIEWING_SEAT_CUSHION","M28_VIEWING_SEAT_BACK")
VIEWS=("gallery_arrival_eye","controlled_threshold_eye")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 files=list(SEED.rglob("M28_EDITABLE_ORBITAL_GALLERY.blend"))
 assert len(files)==1
 assert sha(files[0])==PIN,"Immutable M28 original mismatch"
 return files[0]
def preflight():
 assert not OUT.exists()
 assert len(HIDE)==3
 return str(original())
def run():
 import bpy
 preflight()
 bpy.ops.wm.open_mainfile(filepath=str(original().resolve()))
 scene=bpy.context.scene
 first=set(bpy.data.objects.keys())
 original_cam={}
 for n in VIEWS:
  o=bpy.data.objects.get("M27_CAMERA_"+n)
  assert o and o.type=="CAMERA"
  original_cam[n]=(tuple(o.location),tuple(o.rotation_euler),float(o.data.lens))
 floor=bpy.data.objects.get("M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK")
 door=bpy.data.objects.get("M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD")
 assert floor and door
 def vertices(obj):
  return sorted(tuple(round(float(c),5) for c in obj.matrix_world @ v.co) for v in obj.data.vertices)
 floor_before=vertices(floor)
 door_before=vertices(door)
 changed={}
 def pos(v):return tuple(ORIGIN[i]+v[i] for i in range(3))
 panel=bpy.data.objects.get(SIGN)
 assert panel and panel.type=="MESH" and not panel.hide_render
 changed[SIGN]={"old_location":list(panel.location),"old_dimensions":list(panel.dimensions)}
 panel.location=pos((12.15,-16.00,4.23))
 panel.dimensions=(3.75,.17,.95)
 # Apply geometry scale before saving so external GLB represents the authored change.
 bpy.ops.object.select_all(action="DESELECT")
 panel.select_set(True);bpy.context.view_layer.objects.active=panel
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 changed[SIGN]["new_location"]=list(panel.location)
 changed[SIGN]["new_dimensions"]=list(panel.dimensions)
 for name,p,s in ((HEAD,(10.48,-16.135,4.18),.70),
                  (SUB,(10.55,-16.14,3.89),.76)):
  ob=bpy.data.objects.get(name)
  assert ob and ob.type=="MESH" and not ob.hide_render
  changed[name]={"old_location":list(ob.location),"old_scale":list(ob.scale)}
  ob.location=pos(p)
  ob.scale=tuple(float(x)*s for x in ob.scale)
  changed[name]["new_location"]=list(ob.location)
  changed[name]["new_scale"]=list(ob.scale)
 for name in HIDE:
  o=bpy.data.objects.get(name)
  assert o and o.type=="MESH" and not o.hide_render
  o.hide_render=True
 assert set(bpy.data.objects.keys())==first,"Do not invent new geometry to hide bad layout"
 assert vertices(floor)==floor_before and vertices(door)==door_before
 for n in VIEWS:
  o=bpy.data.objects.get("M27_CAMERA_"+n)
  assert (tuple(o.location),tuple(o.rotation_euler),float(o.data.lens))==original_cam[n]
 scene["M28B"]="DIRECT_REAL_IMAGE_EDIT_3_SIGN_OBJECTS_3_BENCHES_HIDDEN"
 scene["ART"]="HOLD_NOT_APPROVED";scene["ADOPTED"]=0
 scene["FORMAL_331_993"]="NOT_RUN";scene["MINECRAFT_EDUCATION_WRITES"]=0
 OUT.mkdir(parents=True)
 blend=OUT/"M28B_EDITED_HUMAN_GALLERY_SIGHTLINE.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 scene.render.engine="CYCLES";scene.cycles.samples=40
 scene.render.resolution_x=1080;scene.render.resolution_y=680
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format="PNG"
 images={}
 for n in VIEWS:
  scene.camera=bpy.data.objects["M27_CAMERA_"+n]
  f=OUT/("M28B_"+n+".png")
  scene.render.filepath=str(f)
  bpy.ops.render.render(write_still=True)
  assert f.stat().st_size>3000
  images[n]={"sha256":sha(f),"bytes":f.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M28B_GALLERY_REFINEMENT_ART_HOLD.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 record={
  "stage":"M28B_IMAGE_GUIDED_SIGHTLINE_REFINEMENT",
  "source_native_SHA256":PIN,"source_GLB_SHA256":GLB_PIN,
  "changed_exact_three_existing_sign_objects":changed,
  "hidden_exact_three_bench_objects":list(HIDE),
  "new_objects":0,"original_frozen_cameras":True,
  "preserved_public_floor_and_threshold":True,
  "original_M27_room_meshes_unmodified":True,
  "views":images,"blend_sha256":sha(blend),"glb_sha256":sha(glb),
  "art":"HOLD_NOT_APPROVED","adopted":0,"minecraft":"FORBIDDEN",
  "official_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "limitations":"Only two fixed real cameras. No certified human corridor, art acceptance, or construction."
 }
 (OUT/"manifest.json").write_text(json.dumps(record,indent=2,ensure_ascii=False))
 print("M28B_REAL_BLENDER_FIXED_TWO_EYE_EDIT_COMPLETE_ART_HOLD")
if __name__=="__main__":
 if "--preflight" in sys.argv:print("M28B_PINNED_M28",preflight())
 else:run()
