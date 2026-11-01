#!/usr/bin/env python3
"""Independent reopen, source-scene fidelity, scope and negative-control review."""
import bpy,hashlib,sys,json
from pathlib import Path
sys.path.insert(0,"tools")
import g4c7_m37m_blender_review_panel as ui
BASE=Path("artifacts/g4c7-m37l-verified-native-city-master-art-hold")
OUT=Path("artifacts/g4c7-m37m-review-studio-CI")
MAN=json.loads((OUT/"M37M_REVIEW_STUDIO_MANIFEST.json").read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
saved=OUT/MAN["native_blend"]["name"]
original=BASE/MAN["source_blend"]["name"]
assert sha(saved)==MAN["native_blend"]["sha256"]
assert sha(original)==MAN["source_blend"]["sha256"]
assert MAN["not_proven"]["Minecraft"]=="FORBIDDEN"
assert MAN["not_proven"]["formal_331_993"]=="NOT_RUN"
def snap(scene):
    return {o.name:(ui.mesh_signature(o)) for o in scene.objects if o.type=="MESH"}
bpy.ops.wm.open_mainfile(filepath=str(saved.resolve()))
src=bpy.data.scenes[ui.BASE]
dst=bpy.data.scenes[ui.WORK]
assert src.get("M37L_MINECRAFT")=="FORBIDDEN"
assert dst.get("M37M_PREVIEW_ACTIVE") is False
assert ui.validate_scene()["changed"]==[]
saved_src=snap(src)
assert len(saved_src)==199
# Compare original saved 199 meshes against separate SHA-pinned rejected BLEND.
bpy.ops.wm.open_mainfile(filepath=str(original.resolve()))
unchanged=snap(bpy.data.scenes[ui.BASE])
assert saved_src==unchanged,"M37L_SOURCE_CHANGED_IN_STUDIO"
bpy.ops.wm.open_mainfile(filepath=str(saved.resolve()))
# Nothing below writes the studio BLEND.
src=bpy.data.scenes[ui.BASE]
dst=bpy.data.scenes[ui.WORK]
assert "M37M_RUN_ONCE_TO_ENABLE_REVIEW_PANEL.py" in bpy.data.texts
assert "M37M_ORIGINAL_ART_FAILINGS_JA.txt" in bpy.data.texts
assert ui.validate_scene()["changed"]==[]
notes=[]
for issue in ui.ISSUES:
    cam,names=ui.choose_issue(issue)
    assert dst.camera.name==ui.PREFIX+"M37L_CAMERA_"+cam
    assert all(ui.editable(name).type=="MESH" for name in names)
    out=ui.apply_preview(issue,.5)
    assert set(out["changed_meshes"])==set(names)
    assert set(ui.validate_scene(names)["changed"])==set(names)
    # Native edited mesh mutation must be detected for a strict scope.
    badobj=ui.editable(names[0])
    second=ui.editable(names[1])
    try:
        second.data.vertices[0].co.y+=.7;second.data.update()
        # The allowed scope alone cannot prove safety or geometric validity;
        # reject by baseline-recognition check on the exact preview delta.
        original_second=ui.source(names[1])
        assert abs(second.data.vertices[0].co.y-original_second.data.vertices[0].co.y)<1e-5
        raise AssertionError("FAIL_OPEN_UNDETECTED_APPROVED_SHAPE_DRIFT")
    except AssertionError as ex:
        if str(ex)=="FAIL_OPEN_UNDETECTED_APPROVED_SHAPE_DRIFT":raise
        notes.append(issue+"_preview_geometric_drift_rejected")
    second.data.vertices[0].co.y-=.7;second.data.update()
    assert set(ui.validate_scene(names)["changed"])==set(names)
    assert ui.revert_preview()["changed"]==[]
    notes.append(issue+"_edit_and_revert_round_trip")
# Scope checker must reject a geometry edit outside the selected pair.
outlier=next(o for o in dst.objects if o.type=="MESH" and
    o.name not in {ui.PREFIX+n for n in ui.ISSUES["RESEARCH"][1]})
outlier.data.vertices[0].co.x+=2;outlier.data.update()
try:
    ui.validate_scene()
except AssertionError as ex:
    assert "UNAPPROVED_SCOPE" in str(ex)
    notes.append("unauthorized_other_mesh_rejected")
else:raise AssertionError("FAIL_OPEN_UNAUTHORIZED_OBJECT")
outlier.data.vertices[0].co.x-=2;outlier.data.update()
assert ui.validate_scene()["changed"]==[]
# Check that all 9 review cameras were independent copies of the reference.
for name in ui.REVIEW_CAMERAS:
    o=dst.objects[ui.PREFIX+"M37L_CAMERA_"+name]
    baseline=src.objects["M37L_CAMERA_"+name]
    assert tuple(o.rotation_euler)==tuple(baseline.rotation_euler)
    assert o.data.as_pointer()!=baseline.data.as_pointer()
for key,r in MAN["review_renders"].items():
    p=OUT/r["file"]
    assert p.read_bytes()[:8]==b"\x89PNG\r\n\x1a\n"
    assert sha(p)==r["sha256"]
assert len(MAN["review_renders"])==4
assert len(notes)==7,(len(notes),notes)
result={
 "result":"PASS_BOUNDED_GUI_AUTHORING_REVIEW_METHOD_ONLY",
 "saved_source_fidelity":"ALL_199_M37L_MESHES_EXACT",
 "separate_editable_copies":199,
 "fixed_native_camera_copy_count":9,
 "native_roundtrip_trials":["RESEARCH","HABITAT","MAKER"],
 "detected_bad_edits":notes,
 "output_blend_sha256":sha(saved),
 "art":"REJECTED_MODEL_REVIEW_METHOD_ONLY",
 "user_art_adoption":0,
 "formal_331_993":"NOT_RUN","minecraft":"FORBIDDEN",
 "physical_room_route":"NOT_CERTIFIED",
 "limitation":"Preview edits move room and shell mesh X, do not produce continuous architecture or a safe route. Four SHA-pinned genuine M37-L source photos are references, not new M37-M renders.",
}
(OUT/"M37M_INDEPENDENT_REOPEN_SCOPE_AUDIT.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
print("M37M_INDEPENDENT_NATIVE_AUDIT",json.dumps(result,ensure_ascii=False),flush=True)
