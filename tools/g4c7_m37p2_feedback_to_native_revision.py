#!/usr/bin/env python3
"""M37-P2: reversible ONE revision from genuine 3-view feedback to real Blender.

A narrow, allowlisted topology EDIT stage, not a city generator or AI artist.
The source native .blend must exactly match the SHA bound into a report from
three true Cycles views. The feedback must be EARLY_ART_REJECT. The action
plan is data only; NEVER run generated Python, shell, scripts or arbitrary bpy.

Only edits EXISTING meshes (city_macro/habitat) in a COPY. Each action targets
one actual outward-facing face, instead of selecting entire meshes as the
rejected two-cube technical study did. No object creation, no geometry imports,
no world writes, no ART PASS. Max one revision, then inspect visually again.

Blender CLI:
  blender -b --python g4c7_m37p2_feedback_to_native_revision.py -- \
    --source FIRST_PAIRED.blend \
    --feedback P2_REAL_IMAGE_ART_FEEDBACK.json \
    --actions REVIEW_BOUND_ACTIONS.json \
    --out NEW_UNIQUE_DIRECTORY
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

ROLES = {
    "city_macro": "P2_CITY_MACRO_DIRECT_AUTHOR",
    "habitat": "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
}
NORMALS = {
    "TOP": (0, 0, 1),
    "BOTTOM": (0, 0, -1),
    "FRONT": (0, -1, 0),
    "BACK": (0, 1, 0),
    "LEFT": (-1, 0, 0),
    "RIGHT": (1, 0, 0),
}
OPS = {"inset_facing_face", "extrude_facing_face", "shift_facing_face"}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def number(value, lo, hi):
    return type(value) in (int, float) and math.isfinite(value) and lo <= value <= hi

def vector(v):
    return (isinstance(v, list) and len(v) == 3 and
            all(number(n, -4.0, 4.0) for n in v) and
            sum(abs(n) for n in v) >= 0.1)

def validate(plan, feedback, source_sha, feedback_sha):
    """Fail closed on identity, rejection provenance, dimensions and roles."""
    errors = []
    if not isinstance(plan, dict):
        return ["PLAN_NOT_OBJECT"]
    if (not isinstance(feedback, dict) or
            feedback.get("outcome") != "EARLY_ART_REJECT" or
            feedback.get("art") != "HOLD" or
            feedback.get("official_adoptions") != 0 or
            feedback.get("minecraft") != "FORBIDDEN"):
        errors.append("FEEDBACK_MUST_BE_GENUINE_REJECT_HOLD")
    if feedback.get("original_stored_blend_sha256") != source_sha:
        errors.append("FEEDBACK_REFERENCES_DIFFERENT_BLEND")
    if plan.get("source_sha256") != source_sha:
        errors.append("PLAN_SOURCE_SHA_MISMATCH")
    if plan.get("feedback_sha256") != feedback_sha:
        errors.append("PLAN_FEEDBACK_SHA_MISMATCH")
    if plan.get("purpose") != "SINGLE_TECH_REVISION_NOT_ART":
        errors.append("NOT_A_SINGLE_TECH_REVISION")
    required = plan.get("responds_to")
    known = feedback.get("reasons", [])
    if (not isinstance(required, list) or not required or
            not all(isinstance(x, str) and x in known for x in required)):
        errors.append("NO_VERIFIED_EARLY_REJECT_REASON_BINDING")
    if set(plan) - {"source_sha256", "feedback_sha256", "purpose",
                    "responds_to", "art_intent", "actions"}:
        errors.append("UNKNOWN_TOP_LEVEL_CONTROL")
    if not isinstance(plan.get("art_intent"), str) or len(plan["art_intent"].strip()) < 50:
        errors.append("MISSING_REAL_ART_INTENT")
    actions = plan.get("actions")
    if not isinstance(actions, list) or not 2 <= len(actions) <= 8:
        return sorted(set(errors + ["ACTION_COUNT_NOT_2_TO_8"]))
    counts = {k: 0 for k in ROLES}
    for i, a in enumerate(actions):
        tag=f"ACTION_{i}"
        if not isinstance(a, dict):
            errors.append(tag+"_NOT_OBJECT")
            continue
        if set(a) - {"role", "op", "face", "inset", "delta", "why"}:
            errors.append(tag+"_UNKNOWN_ARGUMENT")
        role=a.get("role")
        op=a.get("op")
        facing=a.get("face")
        if role not in ROLES:
            errors.append(tag+"_ROLE_FORBIDDEN")
        else:
            counts[role] += 1
        if op not in OPS:
            errors.append(tag+"_OP_FORBIDDEN")
        if facing not in NORMALS:
            errors.append(tag+"_FACE_FORBIDDEN")
        if not isinstance(a.get("why"), str) or len(a["why"].strip()) < 18:
            errors.append(tag+"_MISSING_AUTHOR_REASON")
        if op == "inset_facing_face":
            if not number(a.get("inset"), 0.08, 0.4):
                errors.append(tag+"_BAD_INSET")
            if set(a) - {"role", "op", "face", "inset", "why"}:
                errors.append(tag+"_UNKNOWN_INSET_ARGUMENTS")
        elif op in ("extrude_facing_face", "shift_facing_face"):
            if not vector(a.get("delta")):
                errors.append(tag+"_BAD_DELTA")
            if set(a) - {"role", "op", "face", "delta", "why"}:
                errors.append(tag+"_UNKNOWN_EDIT_ARGUMENTS")
    if not all(v >= 1 for v in counts.values()):
        errors.append("MUST_EDIT_BOTH_EXISTING_ROLES")
    return sorted(set(errors))

def verify_visual_evidence_files(feedback_path, report):
    """Verify original 3 true PNG bytes again immediately before editing."""
    names = ("AERIAL", "PUBLIC_EYE", "HABITAT_EYE")
    images = report.get("verified_images_sha256")
    if not isinstance(images, dict) or set(images) != set(names):
        raise ValueError("THREE_VERIFIED_REAL_IMAGE_DIGESTS_REQUIRED")
    folder = Path(feedback_path).resolve().parent
    for view in names:
        filename = "P2_PAIRED_NATIVE_" + view + "_NO_ART.png"
        file = folder / filename
        if not file.is_file() or not 64 <= file.stat().st_size <= 2500000:
            raise ValueError("VISUAL_SOURCE_PNG_MISSING_OR_TOO_LARGE_" + view)
        with file.open("rb") as stream:
            if stream.read(8) != b"\x89PNG\r\n\x1a\n":
                raise ValueError("VISUAL_SOURCE_NOT_PNG_" + view)
        if sha(file) != images[view]:
            raise ValueError("VISUAL_SOURCE_CHANGED_SINCE_FEEDBACK_" + view)
    return True


def native_revision(source_path, feedback_path, actions_path, out_dir):
    import bpy
    import bmesh
    from mathutils import Vector
    source = Path(source_path).resolve()
    feed = Path(feedback_path).resolve()
    actions = Path(actions_path).resolve()
    dest = Path(out_dir).resolve()
    if dest.exists():
        raise FileExistsError("APPEND_ONLY_REVISION_DIRECTORY_EXISTS")
    if not source.is_file() or not feed.is_file() or not actions.is_file():
        raise FileNotFoundError("NATIVE_SOURCE_FEEDBACK_AND_ACTIONS_REQUIRED")
    before = sha(source)
    feed_hash = sha(feed)
    report = json.loads(feed.read_text(encoding="utf-8"))
    plan = json.loads(actions.read_text(encoding="utf-8"))
    problems = validate(plan, report, before, feed_hash)
    if problems:
        raise ValueError("REVISION_PLAN_REJECT_HOLD:"+repr(problems))
    # A feedback JSON alone is not sufficient: bind this one local
    # revision to the exact three original genuine PNG byte streams.
    verify_visual_evidence_files(feed, report)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    scene=bpy.context.scene
    if (scene.get("P2_SOURCE_KIND")!="LOCAL_LLM_NATIVE_EDIT_OPERATOR_TRIAL_NOT_GUI_HUMAN" or
        scene.get("P2_ART")!="HOLD" or scene.get("P2_OFFICIAL_ADOPTIONS") != 0 or
        scene.get("P2_MINECRAFT")!="FORBIDDEN" or
        scene.get("P2_REVISION_STUDY_COUNT",0)!=0):
        raise RuntimeError("SOURCE_SCENE_NOT_ONE_REVISION_ELIGIBLE")
    objs={}
    for role, colname in ROLES.items():
        col=bpy.data.collections.get(colname)
        if col is None:
            raise RuntimeError("MISSING_COLLECTION_"+role)
        candidates=[o for o in col.objects if o.type=="MESH"]
        if len(candidates)!=1:
            raise RuntimeError("EXPECTED_ONE_EXISTING_NATIVE_MESH_"+role)
        objs[role]=candidates[0]
    pre={role:{"vertices":len(o.data.vertices),"faces":len(o.data.polygons)}
         for role,o in objs.items()}
    for action in plan["actions"]:
        role=action["role"]
        obj=objs[role]
        bm=bmesh.new()
        try:
            bm.from_mesh(obj.data)
            bm.normal_update()
            if not bm.faces:
                raise ValueError("NO_EXISTING_FACES")
            direction=Vector(NORMALS[action["face"]])
            # Exact author-selected orientation: avoid secretly applying
            # arbitrary global extrusion to all faces (old 2-cube failure).
            f=max(bm.faces, key=lambda face: face.normal.dot(direction))
            if f.normal.dot(direction) < 0.75:
                raise ValueError("REQUESTED_FACE_ORIENTATION_NOT_PRESENT")
            if action["op"] == "inset_facing_face":
                bmesh.ops.inset_region(
                    bm, faces=[f], thickness=action["inset"],
                    depth=0.0, use_even_offset=True)
            elif action["op"] == "extrude_facing_face":
                result=bmesh.ops.extrude_face_region(bm, geom=[f])
                verts=[e for e in result["geom"] if isinstance(e,bmesh.types.BMVert)]
                if not verts:
                    raise RuntimeError("NATIVE_EXTRUDE_HAS_NO_REAL_VERTICES")
                bmesh.ops.translate(bm, verts=list(set(verts)),
                                    vec=Vector(action["delta"]))
            elif action["op"] == "shift_facing_face":
                bmesh.ops.translate(bm, verts=list(f.verts),
                                    vec=Vector(action["delta"]))
            else:
                raise RuntimeError("UNAUTHORIZED_EDIT")
            bm.normal_update()
            if any(len(face.verts)<3 or face.calc_area()<1e-6 for face in bm.faces):
                raise RuntimeError("DEGENERATE_FACE_AFTER_NATIVE_REVISION")
            bm.to_mesh(obj.data)
            obj.data.update()
        finally:
            bm.free()
    post={role:{"vertices":len(o.data.vertices),"faces":len(o.data.polygons)}
          for role,o in objs.items()}
    changed=any(post[role]!=pre[role] for role in ROLES)
    if not changed:
        raise RuntimeError("REVISION_DID_NOT_CHANGE_NATIVE_TOPOLOGY")
    # Source is never saved; a separate .blend and evidence are produced.
    scene["P2_REVISION_STUDY_COUNT"]=1
    scene["P2_REVISION_SOURCE_SHA256"]=before
    scene["P2_REVISION_FEEDBACK_SHA256"]=feed_hash
    scene["P2_REVISION_FORMAL_ART"]="HOLD_NOT_REVIEWED"
    scene["P2_ART"]="HOLD"
    scene["P2_OFFICIAL_ADOPTIONS"]=0
    scene["P2_CAMERA_VIEWS_AUTHOR_APPROVED"]=False
    scene["P2_MINECRAFT"]="FORBIDDEN"
    dest.mkdir(parents=True)
    new_path=dest/"P2_NATIVE_EDITOR_FEEDBACK_REVISION_01_UNAPPROVED.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(new_path),compress=False)
    if sha(source)!=before or sha(feed)!=feed_hash:
        raise RuntimeError("SAVED_SOURCE_OR_VISUAL_FEEDBACK_CHANGED")
    evidence={
        "schema":"g4c7-m37p2-feedback-to-native-revision-v1",
        "result":"ONE_REAL_NATIVE_EDIT_REVISION_CREATED_NOT_ART",
        "source_blend_sha256":before,
        "source_visual_feedback_sha256":feed_hash,
        "new_blend_sha256":sha(new_path),
        "new_blend_filename":new_path.name,
        "roles_before":pre,
        "roles_after":post,
        "action_count":len(plan["actions"]),
        "original_native_scene_modified":False,
        "human_gui_authorship":"NOT_PERFORMED",
        "visual_critique_after_revision":"NOT_YET_PERFORMED",
        "art":"HOLD","official_adoptions":0,
        "formal_331_993":"NOT_RUN","minecraft":"FORBIDDEN",
        "makecode":"NOT_EVALUATED",
    }
    (dest/"P2_NATIVE_REVISION_01_EVIDENCE.json").write_text(
        json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("P2_ONE_NATIVE_FEEDBACK_REVISION_TECH_ONLY_ART_HOLD",
          json.dumps(evidence),flush=True)
    return evidence

def main():
    argv=sys.argv
    argv=argv[argv.index("--")+1:] if "--" in argv else argv[1:]
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--feedback",required=True)
    p.add_argument("--actions",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args(argv)
    return native_revision(args.source,args.feedback,args.actions,args.out)

if __name__=="__main__":
    main()
