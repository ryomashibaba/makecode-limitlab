#!/usr/bin/env python3
"""M37-P2 exploratory native Blender EDIT OPERATOR replay, NOT a city generator.

Unlike the rejected single-shot 11-mesh vertex JSON, this records short,
author-chosen native editor actions. The program NEVER invents a city plan:
it only applies the explicitly supplied operations to an isolated, verified
copy of the original studio. No raw model-generated Python is evaluated.

Limited FIRST PAIR: macro-city silhouette + lived residential section together.
No official art adoption, safety certification, or Minecraft writes. ALL
outputs are technically inspectable ART-HOLD studies, NOT project city meshes.

Blender:
  blender -b --python tools/g4c7_m37p2_native_operator_author.py -- \
    --source PATH_TO_PINNED_V3.blend --actions ACTIONS.json --out NEW_DIRECTORY
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys

V3_SHA = "536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
ROLES = {
    "city_macro": "P2_CITY_MACRO_DIRECT_AUTHOR",
    "habitat": "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
}
OPS = {"begin_surface", "extrude_face", "inset_face", "translate_selection"}
VIEW_NAMES = ["P2_CAMERA_AERIAL", "P2_CAMERA_PUBLIC_EYE", "P2_CAMERA_HABITAT_EYE"]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def valid_vector(value, max_abs=150.0):
    return (isinstance(value, list) and len(value) == 3 and
            all(type(x) in (int, float) and math.isfinite(x)
                and abs(x) <= max_abs for x in value))


def validate_actions(plan):
    """Strict action-only gate. Never execute model prose as code."""
    errors = []
    if not isinstance(plan, dict):
        return ["ACTION_ROOT_NOT_OBJECT"]
    if not isinstance(plan.get("art_intent"), str) or len(plan["art_intent"].strip()) < 40:
        errors.append("ART_INTENT_INSUFFICIENT")
    actions = plan.get("actions")
    if not isinstance(actions, list):
        return errors + ["ACTIONS_NOT_LIST"]
    if not 6 <= len(actions) <= 36:
        errors.append("ACTION_COUNT_OUT_OF_RANGE")
    begun = set()
    counts = Counter()
    for i, a in enumerate(actions[:37]):
        tag = f"ACTION_{i}"
        if not isinstance(a, dict):
            errors.append(tag + "_NOT_OBJECT")
            continue
        role = a.get("role")
        kind = a.get("op")
        if role not in ROLES or kind not in OPS:
            errors.append(tag + "_ROLE_OR_OPERATOR_NOT_ALLOWED")
            continue
        counts[role] += 1
        # Strict schemas disallow arbitrary bpy/python, filepath or other
        # model-driven parameters. This is not an arbitrary-code executor.
        allowed = {"role", "op", "intent", "location", "delta", "thickness"}
        if set(a) - allowed:
            errors.append(tag + "_UNKNOWN_PARAMETERS")
        if not isinstance(a.get("intent"), str) or len(a["intent"].strip()) < 16:
            errors.append(tag + "_NO_VISUAL_REASON")
        if kind == "begin_surface":
            if role in begun:
                errors.append(tag + "_SECOND_SEED_FORBIDDEN")
            begun.add(role)
            if not valid_vector(a.get("location")):
                errors.append(tag + "_BAD_SEED_LOCATION")
            if len([k for k in a if k not in {"role","op","intent","location"}]):
                errors.append(tag + "_SEED_EXTRANEOUS_ARGUMENTS")
        else:
            if role not in begun:
                errors.append(tag + "_EDIT_BEFORE_SEED")
            if kind in ("extrude_face","translate_selection"):
                if not valid_vector(a.get("delta"), 24):
                    errors.append(tag + "_BAD_EDIT_DELTA")
            elif kind == "inset_face":
                thick = a.get("thickness")
                if type(thick) not in (float, int) or not 0.01 <= thick <= 1.5:
                    errors.append(tag + "_BAD_INSET")
    for role in ROLES:
        if role not in begun:
            errors.append("PAIR_MISSING_" + role)
        if counts[role] < 3:
            errors.append("PAIR_NOT_AUTHORED_ENOUGH_" + role)
    # Explicitly prevent consuming this exploratory tool as a complete
    # city or promoting any output into user-approved ART.
    if plan.get("promote_art") or plan.get("world_write"):
        errors.append("FORBIDDEN_PRODUCTION_ACTION")
    return sorted(set(errors))


def native_replay(source, actions, destination):
    import bpy

    original = Path(source).resolve()
    target = Path(destination).resolve()
    if not original.is_file() or sha256(original) != V3_SHA:
        raise RuntimeError("V3_SOURCE_SHA_MISMATCH_REFUSE")
    if target.exists():
        raise FileExistsError("APPEND_ONLY_STUDY_DIRECTORY_EXISTS")
    source_manifest = json.loads(Path(actions).read_text(encoding="utf-8"))
    errors = validate_actions(source_manifest)
    if errors:
        raise ValueError("NATIVE_ART_ACTION_REJECT_HOLD: " + str(errors))
    target.mkdir(parents=True)
    bpy.ops.wm.open_mainfile(filepath=str(original))
    scene = bpy.context.scene
    assert scene.get("P2_ART") == "HOLD"
    assert scene.get("P2_OFFICIAL_ADOPTIONS") == 0
    assert scene.get("P2_MINECRAFT") == "FORBIDDEN"
    assert not any(obj.type == "MESH" for obj in scene.objects)
    objects = {}
    counts = Counter()

    for index, action in enumerate(source_manifest["actions"]):
        role = action["role"]
        op = action["op"]
        collection = bpy.data.collections.get(ROLES[role])
        if collection is None:
            raise RuntimeError("P2_REQUIRED_COLLECTION_MISSING")
        if op == "begin_surface":
            # A native Blender OBJECT/EDIT-mode seed for later *author*
            # manipulation. Never assemble repeated seeded primitives.
            bpy.ops.object.mode_set(mode="OBJECT") if bpy.context.object and bpy.context.object.mode != "OBJECT" else None
            bpy.ops.mesh.primitive_plane_add(size=1.2, location=action["location"])
            obj = bpy.context.object
            obj.name = "P2_EDIT_OPERATOR_UNAPPROVED_" + role
            for c in list(obj.users_collection):
                c.objects.unlink(obj)
            collection.objects.link(obj)
            obj["AUTHORSHIP"] = "AI_ACTION_SEQUENCE_BPY_NATIVE_EDIT_NOT_HUMAN_GUI"
            objects[role] = obj
        else:
            obj = objects.get(role)
            if obj is None or obj.type != "MESH":
                raise RuntimeError("MISSING_AUTHOR_MESH_FOR_EDIT")
            if bpy.context.object and bpy.context.object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action="SELECT")
            if op == "extrude_face":
                bpy.ops.mesh.extrude_region_move(
                    MESH_OT_extrude_region={},
                    TRANSFORM_OT_translate={"value":tuple(action["delta"])})
            elif op == "inset_face":
                bpy.ops.mesh.inset(thickness=action["thickness"], depth=0.0)
            elif op == "translate_selection":
                bpy.ops.transform.translate(value=tuple(action["delta"]))
            bpy.ops.object.mode_set(mode="OBJECT")
        counts[role] += 1

    scene["P2_SOURCE_KIND"] = "LOCAL_LLM_NATIVE_EDIT_OPERATOR_TRIAL_NOT_GUI_HUMAN"
    scene["P2_STUDIO_STAGE"] = "PAIRED_EDITOR_OPERATOR_NON_ART_TRIAL"
    scene["P2_ART"] = "HOLD"
    scene["P2_OFFICIAL_ADOPTIONS"] = 0
    scene["P2_CAMERA_VIEWS_AUTHOR_APPROVED"] = False
    scene["P2_MINECRAFT"] = "FORBIDDEN"
    out_file = target / "P2_NATIVE_EDITOR_PAIRED_STUDY_UNAPPROVED.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(out_file), compress=False)
    result = {
        "status":"PAIRED_NATIVE_OPERATOR_STUDY_CREATED_NOT_ART",
        "native_file":out_file.name,
        "native_sha256":sha256(out_file),
        "original_sha256":sha256(original),
        "action_count":len(source_manifest["actions"]),
        "roles":dict(counts),
        "art":"HOLD","official_adoptions":0,
        "formal_331_993":"NOT_RUN",
        "minecraft":"FORBIDDEN",
        "makecode":"NOT_EVALUATED",
        "camera_views":"NOT_ART_REVIEWED",
        "source_kind":"NATIVE_BPY_OPERATOR_REPLAY_NOT_GUI_DIRECT_HUMAN",
    }
    (target/"P2_OPERATOR_STUDY_HOLD_EVIDENCE.json").write_text(
        json.dumps(result, indent=2)+"\n",encoding="utf-8")
    if sha256(original) != V3_SHA:
        raise RuntimeError("PROTECTED_EMPTY_V3_CHANGED_DURING_TRIAL")
    return result


def main():
    argv = sys.argv
    argv = argv[argv.index("--")+1:] if "--" in argv else argv[1:]
    p = argparse.ArgumentParser()
    p.add_argument("--source")
    p.add_argument("--actions")
    p.add_argument("--out")
    p.add_argument("--validate-only", action="store_true")
    args = p.parse_args(argv)
    if not args.actions:
        p.error("--actions is required")
    if args.validate_only:
        errors = validate_actions(json.loads(Path(args.actions).read_text(encoding="utf-8")))
        print("P2_ACTION_GATE:", json.dumps(errors))
        return 2 if errors else 0
    if not args.source or not args.out:
        p.error("Blender replay requires --source and --out")
    print("P2_PAIRED_NATIVE_OPERATOR_EVIDENCE:",json.dumps(
        native_replay(args.source,args.actions,args.out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
