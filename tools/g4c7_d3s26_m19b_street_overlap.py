#!/usr/bin/env python3
"""M19B: isolated street-eye coplanar overlap A/B experiment.

Source is M19A's native .blend, strictly SHA256 pinned. Only change the local
Z position of two road meshes at the known junction. Cameras, materials,
lights, shader settings and other geometry must remain unchanged. ART HOLD.
"""
import hashlib,json,os,sys
from pathlib import Path
SEED=Path("artifacts/m19b_pinned_m19a_native_seed")
OUT=Path("artifacts/g4c7-m19b-street-junction-overlap-test")/("run_"+os.getenv("GITHUB_SHA","local")[:12])
PIN="9a76deb0437c7b89d95e80024185c597111224b71fe055bc5ea7f1a4da042f79"
VIEWS=("south","north","oblique","district","street_eye","maker_eye","research_eye","resident_eye")
A="M18_TRUE_STREET_01_P1_MARKET_STREET_TO_P2_FORUM"
B="M18_TRUE_STREET_04_P1_MARKET_STREET_TO_P5_MARKET_INTERIOR"
LIFTS={A:.016,B:.036}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 found=list(SEED.rglob("M19A_REVERSED_FLOOR_NORMALS_NATIVE.blend"))
 assert len(found)==1,("Expected exactly one M19A native source",len(found))
 assert sha(found[0])==PIN,"Immutable M19A source mismatch"
 return found[0]
def experiment():
 import bpy
 path=original()
 assert not OUT.exists(),"Append-only output; refuse overwrite"
 bpy.ops.wm.open_mainfile(filepath=str(path.resolve()))
 scene=bpy.context.scene
 before=set(bpy.data.objects.keys())
 before_materials={m.name for m in bpy.data.materials}
 before_lights={o.name:tuple(o.location) for o in bpy.data.objects if o.type=="LIGHT"}
 before_cameras={o.name:(tuple(o.location),tuple(o.rotation_euler),float(o.data.lens))
                for o in bpy.data.objects if o.type=="CAMERA"}
 changes={}
 for name,dz in LIFTS.items():
  ob=bpy.data.objects.get(name)
  assert ob is not None and ob.type=="MESH",(name,"missing target")
  assert len(ob.data.polygons)==1
  normal=float(ob.data.polygons[0].normal.z)
  assert normal>.98,(name,normal)
  old_z=float(ob.location.z)
  assert abs(old_z)<.00001,(name,old_z)
  ob.location.z=old_z+dz
  changes[name]={"original_z":old_z,"edited_z":float(ob.location.z),
                 "delta":dz,"normal_z_unchanged":normal}
 assert len(changes)==2
 assert before==set(bpy.data.objects.keys()),"No objects may be created or removed"
 assert before_materials=={m.name for m in bpy.data.materials}
 assert before_lights=={o.name:tuple(o.location) for o in bpy.data.objects if o.type=="LIGHT"}
 assert before_cameras=={o.name:(tuple(o.location),tuple(o.rotation_euler),float(o.data.lens))
                 for o in bpy.data.objects if o.type=="CAMERA"}
 scene["M19B"]="TWO_COPLANAR_JUNCTION_PAVING_SURFACES_ONLY"
 scene["ART"]="HOLD_NOT_APPROVED";scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["FORMAL_BODY_331_FEET_993"]="NOT_RUN"
 scene["G0_S1_G1_G2_G3"]="NOT_RUN"
 OUT.mkdir(parents=True)
 blend=OUT/"M19B_EDITED_JUNCTION_NATIVE.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 scene.render.engine="CYCLES"
 views={}
 for name in VIEWS:
  camera=bpy.data.objects.get("M18_CAMERA_"+name)
  assert camera is not None and camera.type=="CAMERA"
  scene.camera=camera
  image=OUT/("M19B_"+name+".png")
  scene.render.filepath=str(image)
  bpy.ops.render.render(write_still=True)
  assert image.stat().st_size>1500
  views[name]={"sha256":sha(image),"bytes":image.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M19B_STREET_OVERLAP_TEST_ART_HOLD.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={
  "stage":"M19B_STREET_OVERLAP_EXPERIMENT",
  "pinned_original_sha256":PIN,"native_blend_sha256":sha(blend),
  "glb_sha256":sha(glb),"views":views,"changed_only_road_surface_local_z":changes,
  "camera_material_lights_fixed":True,"zero_new_objects":True,
  "known_prior_street_eye_black_25":8048,
  "known_prior_street_eye_black_in_double_overlaps":8032,
  "prior_classification_note":"Ray-plane and projected street triangle footprint; overlap evidence not by itself causality",
  "art":"HOLD_NOT_APPROVED","adopted":0,"minecraft":"FORBIDDEN",
  "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "disclaimer":"Nonzero delta is a diagnostic only, not a construction-safe grade or approved seamless junction"}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
 print("M19B_TWO_ROAD_PAVEMENT_Z_LIFTS_RENDERED_EIGHT_FIXED_CAMERAS",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:print("M19B_PINNED_SOURCE_PASS",original())
 else:experiment()
