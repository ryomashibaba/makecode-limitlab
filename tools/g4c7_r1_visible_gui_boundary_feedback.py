#!/usr/bin/env python3
"""A single image-gated GUI architectural boundary edit on an ISOLATED rejected R1 study.

It does NOT rehabilitate the rejected city; its only point is to prove that a
visible real Blender architecture-specific decision can be edited with GUI keys
and confirmed in an independently reopened new .blend. No generated geometry.
"""
import bpy
import hashlib
import json
import os
import sys
from pathlib import Path

ORIGINAL_SHA = "cadf0678f7a57636dbebe7432e95d4aae98a2a0cc57215652177d9cbd6ef0e06"
TARGET = "HABITAT: private vestibule divider"
NAME_INITIAL = "R1_REJECTED_ARCHITECTURE_BOUNDARY_GUI_METHOD_SOURCE_NOT_ART.blend"
NAME_EDITED = "R1_REJECTED_ARCHITECTURE_BOUNDARY_GUI_METHOD_EDITED_NOT_ART.blend"

def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for part in iter(lambda: f.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()

def charter(scene):
    for k,v in {"P2_ART":"HOLD","P2_OFFICIAL_ADOPTIONS":0,
                "P2_MINECRAFT":"FORBIDDEN",
                "P2_FORMAL_331_993":"NOT_RUN"}.items():
        assert scene.get(k) == v, "CHARTER_FAIL:"+k

def state():
    return {o.name: [round(float(c), 5) for c in o.location] +
            [round(float(c), 5) for c in o.rotation_euler] +
            [round(float(c), 5) for c in o.scale] +
            [len(o.data.vertices),len(o.data.polygons)]
            for o in bpy.data.objects if o.type == "MESH"}

def prepare():
    assert bpy.app.background
    source = Path(bpy.data.filepath).resolve()
    assert source.name == "R1_CIVIC_ESTUARY_GUI_DIRECT_EDIT_NOT_ART.blend"
    assert digest(source) == ORIGINAL_SHA
    charter(bpy.context.scene)
    target = bpy.data.objects[TARGET]
    assert target.type == "MESH"
    assert len([o for o in bpy.data.objects if o.type == "MESH"]) > 100
    base=Path(os.environ["G4C7_VISUAL_EDIT_OUT"]).resolve()
    assert base.is_dir()
    working=base/NAME_INITIAL
    assert not working.exists()
    original_state=state()
    for o in bpy.data.objects:
        o.select_set(False)
    target.select_set(True)
    bpy.context.view_layer.objects.active=target
    # This is an ISOLATED editing environment for a rejected-source METHOD test.
    # Never claim this copy is a new R1 art candidate.
    scene=bpy.context.scene
    scene["R1_METHOD_ONLY"]=True
    scene["R1_ORIGINAL_ART"]="EARLY_ART_REJECT"
    scene["R1_NOT_FOR_ART_USE"]="NO_REHABILITATION_OF_REJECTED_CITY"
    scene["R1_GUI_TARGET"]=TARGET
    initial={"source_sha256":ORIGINAL_SHA,"target":TARGET,
             "baseline_location":original_state[TARGET][:3],
             "mesh_state_before":original_state,
             "method_only":True,"original_art":"EARLY_ART_REJECT",
             "accepted":False}
    report=base/"METHOD_INPUT_PINNED_BASELINE.json"
    assert not report.exists()
    report.write_text(json.dumps(initial,indent=2,ensure_ascii=False)+"\n")
    assert bpy.ops.wm.save_as_mainfile(filepath=str(working),compress=True)=={"FINISHED"}
    assert digest(source)==ORIGINAL_SHA
    print("ISOLATED_R1_GUI_INPUT_PREPARED_ORIGINAL_UNCHANGED",flush=True)

def watch():
    assert not bpy.app.background
    scene=bpy.context.scene
    charter(scene)
    assert scene.get("R1_METHOD_ONLY") is True
    assert scene.get("R1_ORIGINAL_ART")=="EARLY_ART_REJECT"
    source=Path(bpy.data.filepath).resolve()
    assert source.name==NAME_INITIAL
    expected=os.environ["G4C7_VISUAL_PREPARED_SHA256"]
    assert digest(source)==expected
    folder=Path(os.environ["G4C7_VISUAL_EDIT_OUT"]).resolve()
    dest=folder/NAME_EDITED
    assert dest!=source and not dest.exists()
    baseline=json.loads((folder/"METHOD_INPUT_PINNED_BASELINE.json").read_text())
    x0=float(baseline["baseline_location"][0])
    obj=bpy.data.objects[TARGET]
    assert abs(obj.location.x-x0)<.0001
    def observed():
        if abs(obj.location.x-x0-2.0)>0.025:
            return .2
        if dest.exists():raise RuntimeError("METHOD_OUTPUT_ALREADY_EXISTS")
        assert digest(source)==expected
        assert bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True)=={"FINISHED"}
        assert digest(source)==expected
        report=folder/"GUI_EDITOR_NATIVE_SAVE_METHOD_EVIDENCE.json"
        assert not report.exists()
        report.write_text(json.dumps({
            "mode":"GUI_TRANSFORM_OBSERVED_SAVED_NEW_COPY",
            "gui_action":"G X 2 in VIEW_3D",
            "target":TARGET,
            "old_x":x0,
            "new_x":float(obj.location.x),
            "prepared_source_sha256":expected,
            "new_native_sha256":digest(dest),
            "original_sha256":ORIGINAL_SHA,
            "decision":"METHOD_TECH_ONLY_NOT_ART_OR_ARCHITECTURAL_ACCEPTANCE",
            "original_art":"EARLY_ART_REJECT",
            "art":"HOLD","adoptions":0,
            "construction":"FORBIDDEN"},indent=2,ensure_ascii=False)+"\n")
        print("GUI_ARCHITECTURAL_BOUNDARY_REAL_SAVE_READY",flush=True)
        return None
    bpy.app.timers.register(observed,first_interval=1.0)

def verify():
    assert bpy.app.background
    scene=bpy.context.scene;charter(scene)
    assert scene.get("R1_METHOD_ONLY") is True
    assert scene.get("R1_ORIGINAL_ART")=="EARLY_ART_REJECT"
    target=bpy.data.objects[TARGET]
    root=Path(os.environ["G4C7_VISUAL_EDIT_OUT"]).resolve()
    opened=Path(bpy.data.filepath).resolve()
    assert opened==root/NAME_EDITED
    baseline=json.loads((root/"METHOD_INPUT_PINNED_BASELINE.json").read_text())
    observed=json.loads((root/"GUI_EDITOR_NATIVE_SAVE_METHOD_EVIDENCE.json").read_text())
    assert observed["new_native_sha256"]==digest(opened)
    assert abs(target.location.x-baseline["baseline_location"][0]-2.0)<.03
    current=state()
    old=baseline["mesh_state_before"]
    assert set(current)==set(old),"MESH_SET_CHANGED"
    for name,v in old.items():
        a=current[name]
        if name==TARGET:
            assert abs(a[0]-v[0]-2.0)<.03 and a[1:]==v[1:],"WRONG_GUI_TARGET_OR_TOPOLOGY_CHANGED"
        else:
            assert a==v,"UNAUTHORIZED_MESH_TRANSFORM:"+name
    assert not (root/"INDEPENDENT_REOPEN_METHOD_AUDIT.json").exists()
    report={"result":"SINGLE_VISIBLE_GUI_ARCHITECTURAL_BOUNDARY_INPUT_SAVED_REOPENED",
            "scope":"ISOLATED_REJECTED_CITY_METHOD_NOT_NEW_ART",
            "new_native_sha256":digest(opened),
            "original_source_sha256":ORIGINAL_SHA,
            "unchanged_mesh_count":len(current)-1,
            "only_changed_mesh":TARGET,
            "new_target_location":current[TARGET][:3],
            "previous_art":"EARLY_ART_REJECT","new_art":"NONE",
            "art":"HOLD","adoptions":0,
            "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
            "MakeCode":"NOT_EVALUATED","minecraft":"FORBIDDEN","world_writes":0,
            "work":"NOT_USED","sol":"NOT_USED"}
    (root/"INDEPENDENT_REOPEN_METHOD_AUDIT.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    print("INDEPENDENT_GUI_REOPEN_ONLY_TARGET_TRANSLATED_ALL_OTHER_MESHES_IDENTICAL",flush=True)

if __name__=="__main__":
    action=sys.argv[-1]
    {"prepare":prepare,"watch":watch,"verify":verify}[action]()
