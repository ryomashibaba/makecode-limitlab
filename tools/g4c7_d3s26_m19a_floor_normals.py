#!/usr/bin/env python3
"""M19A: controlled experiment on 12 independently confirmed inverted floor normals.
No camera, material, lighting, architecture or Minecraft edits. ART remains HOLD.
"""
from pathlib import Path
import hashlib,json,os,sys
SEED=Path("artifacts/m19a_immutable_m18b_seed")
OUT=Path("artifacts/g4c7-m19a-floor-normal-test")/("run_"+os.getenv("GITHUB_SHA","local")[:12])
PIN="0132ff967b82144dcf31698de5db736122176c9ae59dc219f04762888f9ade81"
NAMES=[
 "M18_TRUE_STREET_00_P0_GATE_TO_P1_MARKET_STREET",
 "M18_TRUE_STREET_01_P1_MARKET_STREET_TO_P2_FORUM",
 "M18_TRUE_STREET_02_P2_FORUM_TO_P3_GARDEN",
 "M18_TRUE_STREET_03_P3_GARDEN_TO_P4_NORTH_COMMON",
 "M18_TRUE_STREET_04_P1_MARKET_STREET_TO_P5_MARKET_INTERIOR",
 "M18_TRUE_STREET_05_P2_FORUM_TO_P6_MAKER_HALL",
 "M18_TRUE_STREET_06_P2_FORUM_TO_P7_STAIR_SOUTH",
 "M18_UPPER_PHYSICAL_LINK_TO_U0","M18_RESEARCH_VISITOR_SPINE",
 "M18_VISIBLE_UPPER_GARDEN_BRIDGE","M18_UPPER_PUBLIC_SPINE_TO_NORTH",
 "M18_RESIDENTIAL_CONTROLLED_APPROACH"]
VIEWS=("south","north","oblique","district","street_eye","maker_eye","research_eye","resident_eye")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 files=list(SEED.rglob("M18B_EDITED_M18_NATIVE_SCENE.blend"))
 assert len(files)==1,("Expected unique pinned M18B .blend",len(files))
 assert sha(files[0])==PIN,"REFUSE UNPINNED ORIGINAL"
 return files[0]
def run():
 import bpy,bmesh
 orig=original()
 assert not OUT.exists(),"Refuse overwrite"
 bpy.ops.wm.open_mainfile(filepath=str(orig.resolve()))
 scene=bpy.context.scene
 before={x.name for x in bpy.data.objects}
 audit=[]
 for n in NAMES:
  o=bpy.data.objects.get(n)
  assert o and o.type=="MESH",n
  assert len(o.data.polygons)==1,(n,len(o.data.polygons))
  poly=o.data.polygons[0]
  before_z=float(poly.normal.z)
  assert before_z<-0.98,(n,before_z)
  bm=bmesh.new()
  bm.from_mesh(o.data)
  bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
  bm.normal_update()
  bm.to_mesh(o.data)
  bm.free()
  o.data.update()
  after_z=float(o.data.polygons[0].normal.z)
  assert after_z>.98,(n,after_z)
  audit.append({"object":n,"normal_z_before":round(before_z,5),"normal_z_after":round(after_z,5),
                "polygon_count":len(o.data.polygons)})
 assert {x.name for x in bpy.data.objects}==before,"M19A MUST NOT CHANGE OBJECTS"
 assert len(audit)==12
 scene["M19A"]="CONTROLLED_FLOOR_WINDING_REVERSAL_ONLY_ART_HOLD"
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["G0_S1_G1_G2_G3"]="NOT_RUN"
 scene["FORMAL_331_993"]="NOT_RUN"
 OUT.mkdir(parents=True)
 blend=OUT/"M19A_REVERSED_FLOOR_NORMALS_NATIVE.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 scene.render.engine="CYCLES"
 views={}
 for key in VIEWS:
  camera=bpy.data.objects.get("M18_CAMERA_"+key)
  assert camera and camera.type=="CAMERA",key
  scene.camera=camera
  png=OUT/("M19A_"+key+".png")
  scene.render.filepath=str(png)
  bpy.ops.render.render(write_still=True)
  assert png.stat().st_size>1500
  views[key]={"sha256":sha(png),"bytes":png.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for o in bpy.data.objects:
  if o.type=="MESH" and not o.hide_render:o.select_set(True)
 glb=OUT/"M19A_REVISED_NORMALS_ART_HOLD.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={"stage":"M19A","source_sha256":PIN,"blend_sha256":sha(blend),
  "glb_sha256":sha(glb),"views":views,"flipped":audit,
  "intervention":"12 downward public floor normals reversed only",
  "same_cameras":True,"same_materials":True,"same_lights":True,
  "art":"HOLD_NOT_APPROVED","adopted":0,"minecraft":"FORBIDDEN",
  "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "claim":"TECH TEST ONLY; NO WALKABILITY OR ART APPROVAL"}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2))
 print("M19A_12_FLOOR_NORMALS_FLIPPED_NATIVE_EIGHT_CAMERAS_DONE",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:print("M19A_ORIGINAL_PINNED",original(),"floor_count",len(NAMES))
 else:run()
