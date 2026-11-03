#!/usr/bin/env python3
"""R1 native GUI change observer and independent saved-scene renderer.
No generated geometry, no ART verdict, no safety or Minecraft operation.
"""
import bpy,hashlib,json,os,sys
from pathlib import Path

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def require_charter(scene):
    required={"P2_ART":"HOLD","P2_OFFICIAL_ADOPTIONS":0,
      "P2_MINECRAFT":"FORBIDDEN","P2_FORMAL_331_993":"NOT_RUN"}
    for k,v in required.items():
        if scene.get(k)!=v:raise AssertionError("CHARTER_MISMATCH:"+k)
    assert scene.get("R1_UNITS")=="ABSTRACT_RESEARCH_UNITS_NOT_MINECRAFT_BLOCKS"
def watch():
    assert not bpy.app.background,"REAL_GUI_REQUIRED"
    source=Path(bpy.data.filepath).resolve()
    expected=os.environ["G4C7_R1_INITIAL_SHA256"]
    dst=Path(os.environ["G4C7_R1_GUI_NEW_BLEND"]).resolve()
    assert source!=dst and not dst.exists()
    assert sha(source)==expected
    s=bpy.context.scene;require_charter(s)
    obj=bpy.data.objects.get("R1_PUBLIC_LANTERN")
    assert obj is not None and obj.type=="MESH"
    assert abs(obj.location.z)<.0001
    print("READY_FOR_REAL_GUI_R1_OBJECT_TRANSLATION",flush=True)
    def audit_then_save():
        if abs(obj.location.z-1.0)>.045:return .3
        if dst.exists():raise RuntimeError("APPEND_ONLY_SAVE_TARGET_EXISTS")
        assert sha(source)==expected
        assert bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)=={'FINISHED'}
        report=dst.parent/"R1_GUI_REAL_INPUT_OBSERVED.json"
        assert not report.exists()
        report.write_text(json.dumps({
          "stage":"ACTUAL_X11_GUI_GZ_1_OBSERVED_BEFORE_NATIVE_SAVE",
          "note":"Only small canopy elevation GUI edit. City geometry elsewhere is code assisted; no expert autonomous GUI modelling claim.",
          "source_sha256":expected,"gui_saved_sha256":sha(dst),
          "object":"R1_PUBLIC_LANTERN","observed_location_z":obj.location.z,
          "art":"HOLD","official_adoptions":0,"formal_safety":"NOT_RUN",
          "minecraft":"FORBIDDEN","human_artist_approval":False
        },indent=2,ensure_ascii=False)+"\n")
        print("R1_GUI_REAL_TRANSLATE_AND_NATIVE_SAVE_VERIFIED",flush=True)
        return None
    bpy.app.timers.register(audit_then_save,first_interval=1.5)
def review():
    assert bpy.app.background,"INDEPENDENT_BACKGROUND_PROCESS_REQUIRED"
    s=bpy.context.scene;require_charter(s)
    root=Path(os.environ["G4C7_R1_DIR"]).resolve()
    saved=Path(bpy.data.filepath).resolve()
    assert saved.name=="R1_CIVIC_ESTUARY_GUI_DIRECT_EDIT_NOT_ART.blend"
    proof=root/"R1_GUI_REAL_INPUT_OBSERVED.json"
    p=json.loads(proof.read_text())
    assert p["gui_saved_sha256"]==sha(saved)
    obj=bpy.data.objects["R1_PUBLIC_LANTERN"]
    assert abs(obj.location.z-1.0)<.04
    assert len([o for o in s.objects if o.type=="MESH"])>95
    required=["FACTORY: continuous transparent safety partition",
      "PRODUCTION: orbital vehicle hull core 0",
      "PRODUCTION: orbital vehicle hull core 1",
      "PRODUCTION: orbital vehicle hull core 2",
      "HABITAT: front entrance door with physical swing clearance",
      "HABITAT: private vestibule divider",
      "HABITAT: actual exterior city window",
      "HABITAT: living couch",
      "RESEARCH: open review laboratory floor",
      "CULTURE: public gallery exhibition wall",
      "PUBLIC: continuous inhabited esplanade 0"]
    for key in required:
        assert bpy.data.objects.get(key) is not None,"MISSING_MEANINGFUL_SOURCE:"+key
    for name in ("AERIAL","PUBLIC_EYE","HABITAT_EYE"):
        c=bpy.data.objects.get("R1_CAMERA_"+name)
        assert c and c.type=="CAMERA"
        s.camera=c
        s.render.filepath=str(root/(name+"_TRUE_BLENDER_CYCLES.png"))
        bpy.ops.render.render(write_still=True)
        assert (root/(name+"_TRUE_BLENDER_CYCLES.png")).stat().st_size>3000
    report={
      "verdict":"NATIVE_TECH_EVIDENCE_ONLY_ART_JUDGEMENT_REQUIRED",
      "r1_art":"HOLD","user_adoptions":0,
      "saved_native_sha256":sha(saved),
      "protected_original_sha256_expected":"536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249",
      "object_count":len(s.objects),"mesh_count":len([o for o in s.objects if o.type=="MESH"]),
      "public_eye_from_same_saved_native":True,
      "habitat_eye_from_same_saved_native":True,
      "aerial_from_same_saved_native":True,
      "actual_gui_input_evidence_sha256":sha(proof),
      "formal_331_993":"NOT_RUN","gates_G0_S1_G1_G2_G3":"NOT_RUN",
      "world_writes":0,"minecraft":"FORBIDDEN",
      "actual_functional_walk_safety":"NOT_TESTED",
      "structural_egress_fire_safety":"NOT_TESTED",
      "production_equipment_realworld_operability":"NOT_CERTIFIED",
      "method_disclosure":"code-assisted authored mesh source, then one demonstrable real GUI transform; not autonomous sophisticated GUI sculpting",
      "visual_acceptance":"USER_ONLY"
    }
    q=root/"R1_INDEPENDENT_NATIVE_AND_RENDER_AUDIT.json"
    assert not q.exists()
    q.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print("R1_THREE_REAL_CYCLES_RENDERED_FROM_ONE_INDEPENDENT_REOPENED_NATIVE_ART_NOT_YET_EVALUATED",flush=True)
if __name__=="__main__":
    op=sys.argv[-1]
    if op=="watch":watch()
    elif op=="render":review()
    else:raise RuntimeError("expected watch|render")
