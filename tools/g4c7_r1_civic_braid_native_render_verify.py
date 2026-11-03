#!/usr/bin/env python3
"""Independent reopen / five true Blender Cycles views of a single R1 district.

Never auto-promotes to ART PASS. No geometry alterations, no safety / Minecraft.
"""
import bpy,hashlib,json,os,sys
from pathlib import Path
from mathutils import Vector
D=Path(os.environ["G4C7_BRAID_DIR"]).resolve()
SRC=D/"R1_CIVIC_BRAID_AUTHORIAL_SECTION_ART_UNREVIEWED.blend"
assert bpy.app.background and Path(bpy.data.filepath).resolve()==SRC
s=bpy.context.scene
for key,value in {"P2_ART":"HOLD","P2_OFFICIAL_ADOPTIONS":0,"P2_MINECRAFT":"FORBIDDEN","P2_FORMAL_331_993":"NOT_RUN","R1_STATUS":"UNREVIEWED_EARLY_ART_TRIAL"}.items():
 assert s.get(key)==value,(key,s.get(key))
def hashfile(f):
 h=hashlib.sha256()
 with Path(f).open("rb") as stream:
  for part in iter(lambda:stream.read(1024*1024),b""):h.update(part)
 return h.hexdigest()
for name in (
 "HABITAT actual entrance door",
 "HABITAT threshold vestibule divider leading to living room",
 "HABITAT openable exterior south sash",
 "HABITAT actual soft upholstered living sofa",
 "MANUFACTURE actual cylindrical tank hull 0",
 "MANUFACTURE actual overhead bridge crane 0",
 "FACTORY physical one-direction transparent separation",
 "PUBLIC FACTORY visitor gallery traversable floor",
 "RESEARCH folded high-window designed roof and facade",
 "PUBLIC narrow walk street and urban activity 00",
 "STREETWALL: Habitat stepped walled garden",
 "STREETWALL: Public arts archive"
): assert bpy.data.objects.get(name),("MISSING_REQUIRED_SAME_NATIVE_COMPONENT",name)
views=["AERIAL","PUBLIC_EYE","HABITAT_EYE","FACTORY_EYE","RESEARCH_EYE"]
sources=[]
for name in views:
 camera=bpy.data.objects.get("CAM_"+name)
 assert camera and camera.type=="CAMERA"
 s.camera=camera
 path=D/(name+"_CYCLES_TRUE_NATIVE.png")
 assert not path.exists()
 s.render.filepath=str(path)
 bpy.ops.render.render(write_still=True)
 assert path.is_file() and path.stat().st_size>5000
 sources.append({"view":name,"file":path.name,"sha256":hashfile(path),"size_bytes":path.stat().st_size,
                 "camera_location":list(camera.location)})
report={
 "schema":"g4c7-r1-civic-braid-single-native-reopen-art-review-v1",
 "native_file":SRC.name,
 "native_sha256":hashfile(SRC),
 "source":"EXPLICIT_AUTHORIAL_CONTROL_POINTS_WITH_PROGRAMMATIC_MESH_ENCODING",
 "scope":"ONE_INTEGRATED_CITY_SECTION_NOT_A_COMPLETE_GIANT_CITY",
 "main_city_programs":["inhabited streets","real interior","spaceship factory equipment and gallery partition","public research and culture"],
 "five_true_cycles_from_one_native":sources,
 "mesh_objects":len([ob for ob in s.objects if ob.type=="MESH"]),
 "art":"HOLD","official_art_adoptions":0,
 "visual_quality":"NOT_YET_HUMAN_OR_VISION_REVIEWED",
 "R1_art_pass":False,"R1_safety_pass":False,
 "formal_331_body_993_foot":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
 "world_writes":0,"minecraft":"FORBIDDEN","work":"NOT_USED","sol":"NOT_USED",
 "protected_v3_expected_sha256":"536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249",
 "rejected_civic_estuary_expected_sha256":"cadf0678f7a57636dbebe7432e95d4aae98a2a0cc57215652177d9cbd6ef0e06"
}
outfile=D/"INDEPENDENT_SAME_NATIVE_FIVE_TRUE_CYCLES_AUDIT.json"
assert not outfile.exists()
outfile.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print("FIVE_TRUE_CYCLES_SINGLE_NATIVE_ART_HOLD_UNREVIEWED",flush=True)
