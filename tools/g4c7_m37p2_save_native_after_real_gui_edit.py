#!/usr/bin/env python3
"""GUI-only post-input native save gate; NEVER mutates meshes or creates city art.
Wait for the actual GUI-transformed Suzanne before writing a NEW .blend file.
"""
import bpy,hashlib,json,math,os
from pathlib import Path
ORIGINAL="536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def start():
    if bpy.app.background:raise RuntimeError("REAL_GUI_ONLY_NOT_BACKGROUND")
    source=Path(bpy.data.filepath).resolve()
    expected=os.environ["G4C7_PREPARED_GUI_SHA"]
    dest=Path(os.environ["G4C7_NATIVE_SAVE_AS"]).resolve()
    if not source.is_file() or sha(source)!=expected or dest.exists() or dest==source:
        raise RuntimeError("PINNED_PREPARED_NATIVE_SOURCE_OR_NEW_DEST_MISMATCH")
    s=bpy.context.scene
    if s.get("P2_ART")!="HOLD" or s.get("P2_OFFICIAL_ADOPTIONS")!=0 or s.get("P2_MINECRAFT")!="FORBIDDEN":
        raise RuntimeError("FIXED_CHARTER_UNCONFIRMED")
    def observe():
        o=bpy.data.objects.get("Suzanne")
        if o is None or o.type!="MESH" or len(o.data.vertices)!=507:return .18
        if (abs(o.location.x-8)>.02 or abs(o.location.y-5)>.02 or
            abs(o.scale.x-1.3)>.02 or abs(o.scale.y-1.3)>.02 or
            abs(o.rotation_euler.z-math.radians(30))>.02):
            return .18
        if dest.exists():raise FileExistsError("NATIVE_STAGE2_APPEND_ONLY")
        result=bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True)
        if "FINISHED" not in result or not dest.is_file() or sha(source)!=expected:
            raise RuntimeError("SAVE_FAILED_OR_PREPARED_SOURCE_MUTATED")
        record=dest.parent/"GUI_POST_INPUT_SAVE_EVIDENCE.json"
        if record.exists():raise FileExistsError("EVIDENCE_ALREADY_EXISTS")
        record.write_text(json.dumps({
          "status":"ACTUAL_GUI_TRANSFORM_OBSERVED_THEN_NATIVE_SAVE_COPY",
          "source_prepared_sha256":expected,"new_saved_sha256":sha(dest),
          "vertices":len(o.data.vertices),"x":float(o.location.x),"y":float(o.location.y),
          "scale":float(o.scale.x),"z_rotation_degrees":math.degrees(o.rotation_euler.z),
          "mesh_generated_by_this_saver":False,"no_gui_input_generated_by_saver":True,
          "art":"HOLD","official_adoptions":0,"minecraft":"FORBIDDEN"
        },indent=2)+"\n")
        print("REAL_GUI_EDIT_NATIVE_COPY_SAVED_AFTER_TRANSFORM_GATE",flush=True)
        return None
    bpy.app.timers.register(observe,first_interval=1.5)
start()
