#!/usr/bin/env python3
"""M29B: change ONLY an already-existing NEW M29 exterior camera.
One visitor-exit eye instead of a camera dominated by grey empty sky.
M28B comparison cameras, mesh objects, materials, lighting stay pinned.
"""
import json,hashlib,os,sys
from pathlib import Path
SEED=Path("artifacts/m29b_immutable_m29")
OUT=Path("artifacts/g4c7-m29b-exit-human-eye")/("run_"+os.environ.get("GITHUB_SHA","local")[:12])
PIN="eae814098136f291c2d0c01fd327a711fbaf97296ec9d9e31527927641044cdc"
LOCAL_ORIGIN=(-43.,37.,9.6)
TARGET="M29_OUTDOOR_COURT_CAMERA"
FROZEN=("M27_CAMERA_gallery_arrival_eye","M27_CAMERA_controlled_threshold_eye")
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def original():
 a=list(SEED.rglob("M29_EDITABLE_OPEN_AIR_RESEARCH_COURT.blend"))
 assert len(a)==1,"M29 native artifact must be unique"
 assert sha(a[0])==PIN,"M29 native source mismatch"
 return a[0]
def preflight():
 assert not OUT.exists()
 return str(original())
def main():
 import bpy
 from mathutils import Vector
 preflight()
 bpy.ops.wm.open_mainfile(filepath=str(original().resolve()))
 scene=bpy.context.scene
 all_objects=set(o.name for o in bpy.data.objects)
 before_frozen={n:(tuple(bpy.data.objects[n].location),
  tuple(bpy.data.objects[n].rotation_euler),float(bpy.data.objects[n].data.lens)) for n in FROZEN}
 frozen_meshes={o.name:len(o.data.vertices) for o in bpy.data.objects if o.type=="MESH"}
 c=bpy.data.objects.get(TARGET)
 assert c and c.type=="CAMERA"
 oldcam={"location":list(c.location),"rotation":list(c.rotation_euler),"lens":float(c.data.lens)}
 def world(p):return Vector(tuple(LOCAL_ORIGIN[i]+p[i] for i in range(3)))
 c.location=world((22.0,-13.7,1.72))
 look=world((37.3,9.0,3.15))
 c.rotation_euler=(look-c.location).to_track_quat("-Z","Y").to_euler()
 c.data.lens=30.0
 bpy.context.view_layer.update()
 assert set(o.name for o in bpy.data.objects)==all_objects
 assert frozen_meshes=={o.name:len(o.data.vertices) for o in bpy.data.objects if o.type=="MESH"}
 for n in FROZEN:
  ob=bpy.data.objects[n]
  assert before_frozen[n]==(tuple(ob.location),tuple(ob.rotation_euler),float(ob.data.lens))
 scene.camera=c
 scene.render.engine="CYCLES";scene.cycles.samples=34
 scene.render.resolution_x=1080;scene.render.resolution_y=680
 scene.render.resolution_percentage=100;scene.render.image_settings.file_format="PNG"
 scene["M29B"]="DIAGNOSTIC_ONLY_SAME_MODEL_NEW_EXIT_EYE_ART_HOLD"
 scene["ART"]="HOLD_NOT_APPROVED";scene["ADOPTED"]=0
 scene["OFFICIAL_331_993"]="NOT_RUN";scene["MINECRAFT_EDUCATION_WRITES"]=0
 OUT.mkdir(parents=True)
 blend=OUT/"M29B_EDITABLE_HUMAN_EXIT_VIEW_ONLY.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 png=OUT/"M29B_OPEN_AIR_FROM_GALLERY_EXIT.png"
 scene.render.filepath=str(png);bpy.ops.render.render(write_still=True)
 assert png.stat().st_size>2500
 report={"stage":"M29B_SINGLE_CAMERA_COMPOSITION_DIAGNOSTIC",
 "pinned_M29_native_SHA256":PIN,
 "changed_only_camera":TARGET,"old_camera":oldcam,
 "new_camera":{"location":list(c.location),"lens":float(c.data.lens)},
 "frozen_comparison_cameras":list(FROZEN),
 "geometry_edit_count":0,"mesh_count":len(frozen_meshes),
 "new_objects":0,
 "blend_sha256":sha(blend),"png_sha256":sha(png),
 "art":"HOLD_NOT_APPROVED","adopted":0,
 "formal_331_993":"NOT_RUN","minecraft":"FORBIDDEN",
 "limitation":"Camera-only diagnostic. Changing view does not prove architectural quality or formal access."}
 (OUT/"manifest.json").write_text(json.dumps(report,indent=2,ensure_ascii=False))
 print("M29B_TRUE_NATIVE_EXTERIOR_EXIT_ONE_EYE_ART_HOLD")
if __name__=="__main__":
 if "--preflight" in sys.argv:print("PINNED_M29_NATIVE",preflight())
 else:main()
