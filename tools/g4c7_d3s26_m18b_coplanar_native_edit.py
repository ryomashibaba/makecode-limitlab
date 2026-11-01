#!/usr/bin/env python3
"""M18B: correct diagnosed coplanar floor z-fighting in actual M18 native blend.
Original is immutable. Only per-surface epsilon offsets; no new city shapes.
"""
from pathlib import Path
import os,sys,json,hashlib
SEED=Path("artifacts/m18b_original_native")
OUT=Path("artifacts/g4c7-m18b-coplanar-qa")/("run_"+os.environ.get("GITHUB_SHA","local")[:12])
PIN="4de9289bb5e36bb704679af9c073451030f6688f680f532959cf1dca0c24dad9"
VIEWS=("south","north","oblique","district","street_eye","maker_eye","research_eye","resident_eye")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 matches=list(SEED.rglob("M18_EDITABLE_OCCUPIED_CIVIC_FABRIC.blend"))
 assert len(matches)==1,("expected unique M18 source",len(matches))
 assert sha(matches[0])==PIN,"Do not modify source"
 return matches[0]
def work():
 import bpy
 from mathutils import Vector
 src=original()
 assert not OUT.exists(),"append-only output"
 bpy.ops.wm.open_mainfile(filepath=str(src.resolve()))
 scene=bpy.context.scene
 # Move frontmost destination surfaces slightly above coincident street surfaces.
 # This is a visual z-fighting fix, NOT a formal safety/ground clearance adjustment.
 lifts={
 "M18_FORUM_NONSYMMETRIC_COURT":.035,
 "M18_MAKER_TRUE_INTERIOR_FLOOR":.055,
 "M18_MARKET_TRUE_OCCUPIED_FLOOR":.055,
 "M18_CIVIC_COURT_OPEN_SKY_PLANTING":.070,
 "M18_MAKER_OCCUPIED_OVERLOOK":.035,
 "M18_RESEARCH_OBSERVER_INHABITED_PLATFORM":.050,
 "M18_RESEARCH_REAL_WORKROOM":.060,
 "M18_OCCUPIED_SKY_GARDEN_TERRACE":.070,
 "M18_RESIDENTIAL_THRESHOLD_REAL_FLOOR":.080,
 }
 for n,delta in lifts.items():
  ob=bpy.data.objects.get(n)
  assert ob and ob.type=="MESH" and len(ob.data.vertices)>=3,n
  assert ob.location.length<1e-5,n
  for v in ob.data.vertices:v.co.z+=delta
  ob.data.update()
 # Restore room-specific composition: original research and reception eye looked
 # at almost exclusively floor, not at their occupied destinations.
 changes={
 "research_eye":((-32,29,11.3),(-47,35,11.9),30),
 "resident_eye":((32,42,11.3),(35,43,10.7),30)}
 for name,(eye,target,lens) in changes.items():
  ob=bpy.data.objects.get("M18_CAMERA_"+name)
  assert ob and ob.type=="CAMERA"
  ob.location=eye
  ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
  ob.data.lens=lens
 # Keep unchanged six cameras for strict visual before/after.
 scene["M18B"]="COPLANAR_SURFACE_QA_REVIEW_ONLY"
 scene["FORMAL_G0_S1_G1_G2_G3"]="NOT_RUN"
 scene["ART"]="HOLD_NOT_APPROVED"
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 OUT.mkdir(parents=True)
 blend=OUT/"M18B_EDITED_M18_NATIVE_SCENE.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 scene.render.engine="CYCLES"
 scene.cycles.samples=11
 views={}
 for name in VIEWS:
  scene.camera=bpy.data.objects["M18_CAMERA_"+name]
  img=OUT/("M18B_"+name+".png")
  scene.render.filepath=str(img)
  bpy.ops.render.render(write_still=True)
  assert img.stat().st_size>1500
  views[name]={"sha256":sha(img),"bytes":img.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M18B_COPLANAR_CORRECTED_UNAPPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 assert glb.stat().st_size>3000
 manifest={"stage":"M18B","source_sha256":PIN,"blend_sha256":sha(blend),
           "glb_sha256":sha(glb),"views":views,"offsets_design_units":lifts,
           "camera_changed":list(changes),"art":"HOLD_NOT_APPROVED","adopted":0,
           "formal_safety":"NOT_RUN","minecraft":"FORBIDDEN",
           "note":"No city-scale form revised; targeted visual QA correction only."}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
 print("M18B_TRUE_NATIVE_ZFIGHT_FIX_AND_EIGHT_VIEW_COMPLETE",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:print("M18B_PINNED_SOURCE_PASS",original())
 else:work()
