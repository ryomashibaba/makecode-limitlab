#!/usr/bin/env python3
"""Actual Blender 4.5 DISPLAY/UI smoke (Xvfb), never city generation.

Runs in a GUI Blender binary (NOT --background), opens the pinned immutable
empty P2 v3 studio, registers its embedded dual-editor operator, SPLITS the
actual 3D View area, changes PUBLIC_EYE -> HABITAT_EYE, and proves the two
areas point to the same unmodified scene. Never saves .blend or creates art.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

SOURCE = Path(
    "artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/"
    "M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend"
)
SHA256 = "536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
JSON_PATH = Path(os.environ.get("P2_GUI_EVIDENCE", "/tmp/g4c7-p2-gui-dual-view.json"))
STATE = {"tick": 0, "ui_split_invoked": False, "ui_split_success": False,
         "public_view_success": False, "habitat_view_success": False}
MODULE = None
WINDOW = None
SCREEN = None


def file_sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as s:
        for chunk in iter(lambda: s.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_immutable(scene):
    if file_sha(SOURCE) != SHA256:
        raise AssertionError("PINNED_V3_SOURCE_CHANGED")
    if any(obj.type == "MESH" for obj in scene.objects):
        raise AssertionError("GUI_SMOKE_MUST_NOT_CREATE_CITY_MESHES")
    for key, val in {
        "P2_ART": "HOLD", "P2_OFFICIAL_ADOPTIONS": 0,
        "P2_FORMAL_331_993": "NOT_RUN", "P2_MINECRAFT": "FORBIDDEN",
        "P2_STUDIO_STAGE": "EMPTY_NO_ART_CREATED",
    }.items():
        if scene.get(key) != val:
            raise AssertionError("P2_SAFETY_ART_CHARTER_VIOLATED:" + key)


def finalize(outcome, detail=None):
    import bpy
    report = {
        "schema": "g4c7-m37p2-real-gui-two-editors-native-v1",
        "outcome": outcome,
        "detail": detail,
        "runtime": list(bpy.app.version),
        "headless": bool(bpy.app.background),
        "real_os_display": os.environ.get("DISPLAY", "MISSING"),
        "camera_focus_cycle": {
            "public_eye": STATE["public_view_success"],
            "habitat_eye": STATE["habitat_view_success"],
        },
        "native_viewport_split": STATE["ui_split_success"],
        "real_3d_view_area_count": len(
            [a for a in SCREEN.areas if a.type == "VIEW_3D"]
        ) if SCREEN else 0,
        "original_blend_sha256": file_sha(SOURCE),
        "geometry_art": "NOT_CREATED",
        "art": "HOLD", "official_adoptions": 0,
        "formal_331_993": "NOT_RUN", "Minecraft": "FORBIDDEN",
        "manual_artist_work": "NOT_PERFORMED",
        "file_writes": "EVIDENCE_JSON_ONLY_NO_BLENDER_SAVE",
    }
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("P2_REAL_GUI_SMOKE_FINAL", json.dumps(report), flush=True)
    # GUI app must exit without offering to save a changed .blend.
    os._exit(0 if outcome == "PASS_ACTUAL_DISPLAY_SPLIT" else 12)


def area_override(context, area):
    import bpy
    region = next((r for r in area.regions if r.type == "WINDOW"), None)
    kwargs = dict(window=WINDOW, screen=SCREEN, area=area)
    if region is not None:
        kwargs["region"] = region
    return bpy.context.temp_override(**kwargs)


def timer_check():
    import bpy
    try:
        STATE["tick"] += 1
        if STATE["tick"] > 22:
            finalize("FAIL_TIMEOUT_WAITING_FOR_REAL_VIEWPORT_SPLIT")
        assert_immutable(bpy.context.scene)
        areas = sorted([a for a in SCREEN.areas if a.type == "VIEW_3D"],
                       key=lambda a: a.x)
        if len(areas) < 2:
            return 0.4
        STATE["ui_split_success"] = True
        assert MODULE["arrange"](SCREEN, bpy.context.scene, "PUBLIC_EYE")
        assert areas[0].spaces.active.region_3d.view_perspective == "PERSP"
        assert areas[1].spaces.active.region_3d.view_perspective == "PERSP"
        STATE["public_view_success"] = True
        scene = bpy.context.scene
        scene.p2_parallel_human_focus = "HABITAT_EYE"
        with area_override(bpy.context, areas[0]):
            result = bpy.ops.g4c7.p2_parallel_refresh()
        if "FINISHED" not in result:
            raise AssertionError("NATIVE_GUI_REFRESH_OPERATOR_FAILED:" + repr(result))
        STATE["habitat_view_success"] = True
        assert_immutable(scene)
        finalize("PASS_ACTUAL_DISPLAY_SPLIT")
    except BaseException:
        finalize("FAIL_REAL_GUI_OPERATOR", traceback.format_exc())
    return None


def main():
    global MODULE, WINDOW, SCREEN
    import bpy
    if os.environ.get("CI") != "true" or not os.environ.get("DISPLAY"):
        raise SystemExit("MUST_RUN_ONLY_IN_DISPLAY_BACKED_CI")
    if bpy.app.background:
        raise SystemExit("NOT_REAL_BLENDER_GUI_BACKGROUND_MODE_FORBIDDEN")
    if bpy.app.version[:2] != (4, 5):
        raise SystemExit("REQUIRES_PINNED_BLENDER_45_GUI")
    if not SOURCE.is_file() or file_sha(SOURCE) != SHA256:
        raise SystemExit("PINNED_NATIVE_V3_SOURCE_MISSING")
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE.resolve()))
    scene = bpy.context.scene
    assert_immutable(scene)
    WINDOW = bpy.context.window or next(iter(bpy.context.window_manager.windows), None)
    if WINDOW is None:
        raise SystemExit("REAL_WINDOW_UNAVAILABLE")
    SCREEN = WINDOW.screen
    areas = [a for a in SCREEN.areas if a.type == "VIEW_3D"]
    if not areas:
        raise SystemExit("REAL_3D_VIEW_AREA_NOT_PRESENT_IN_AUTHOR_STUDIO")
    code = bpy.data.texts["M37P2_RUN_ONCE_PARALLEL_MACRO_LIVED_GUI.py"].as_string()
    MODULE = {"__name__": "m37p2_gui_split_native_test",
              "__file__": "EMBEDDED_TEXT_NOT_DISK"}
    exec(compile(code, "M37P2_RUN_ONCE_PARALLEL_MACRO_LIVED_GUI.py", "exec"), MODULE)
    MODULE["register"]()
    with area_override(bpy.context, areas[0]):
        result = bpy.ops.g4c7.p2_parallel_split()
    if "FINISHED" not in result:
        raise RuntimeError("REAL_SPLIT_OPERATOR_RETURNED:" + repr(result))
    STATE["ui_split_invoked"] = True
    print("P2_REAL_GUI_SPLIT_REQUEST_SENT", flush=True)
    bpy.app.timers.register(timer_check, first_interval=1.4)


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        print("P2_REAL_GUI_INITIALIZATION_ERROR", traceback.format_exc(), flush=True)
        os._exit(15)
