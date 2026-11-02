#!/usr/bin/env python3
"""M37-P2: package the existing EMPTY native .blend as a single-file artist workspace.

No city meshes, geometry, artistic images, or automatic editing. The two GUI
scripts are embedded only as Blender Text data and must be run by an artist.
The archived empty original and all rejected research artifacts remain immutable.
"""
from pathlib import Path
import hashlib
import json
import sys

ORIGINAL = Path("artifacts/g4c7-m37p2-empty-direct-author-studio-ART-NOT-CREATED/M37P2_EMPTY_DIRECT_AUTHOR_MASTER_NOT_ART.blend")
ORIGINAL_SHA256 = "d13e17fb59763a0719b5a91ed80043dade0f40ea65b7a29eba4e5bbfb9545041"
SCRIPTS = {
    "M37P2_RUN_ONCE_PARALLEL_MACRO_LIVED_GUI.py":
        Path("tools/g4c7_m37p2_parallel_author_view.py"),
    "M37P2_NATIVE_THREE_CAMERA_EARLY_REVIEW_NOT_ART.py":
        Path("tools/g4c7_m37p2_author_native_early_review.py"),
}
ARTIFACT = Path("artifacts/g4c7-m37p2-integrated-native-author-workspace-NOT-ART")
OUTPUT = ARTIFACT / "M37P2_INTEGRATED_EMPTY_ARTIST_WORKSPACE_NOT_ART.blend"


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    import bpy

    if not ORIGINAL.is_file() or hash_file(ORIGINAL) != ORIGINAL_SHA256:
        raise RuntimeError("PINNED_EMPTY_SOURCE_MISSING_OR_MUTATED")
    if OUTPUT.exists():
        raise RuntimeError("APPEND_ONLY_OUTPUT_ALREADY_EXISTS")
    if not all(p.is_file() for p in SCRIPTS.values()):
        raise RuntimeError("REQUIRED_AUTHOR_EDITOR_SCRIPTS_MISSING")

    bpy.ops.wm.open_mainfile(filepath=str(ORIGINAL.resolve()))
    scene = bpy.context.scene
    if scene.get("P2_SOURCE_KIND") != "UNAUTHORED_EMPTY_TEMPLATE":
        raise RuntimeError("NOT_AN_EMPTY_NATIVE_ARTIST_MASTER")
    if scene.get("P2_STUDIO_STAGE") != "EMPTY_NO_ART_CREATED":
        raise RuntimeError("DO_NOT_PACK_ART_AS_EMPTY")
    if scene.get("P2_ART") != "HOLD" or scene.get("P2_OFFICIAL_ADOPTIONS") != 0:
        raise RuntimeError("ART_CHARER_VIOLATION")
    if scene.get("P2_MINECRAFT") != "FORBIDDEN" or scene.get("P2_FORMAL_331_993") != "NOT_RUN":
        raise RuntimeError("SAFETY_CHARTER_VIOLATION")
    if any(obj.type == "MESH" for obj in scene.objects):
        raise RuntimeError("EMPTY_ARTIFACT_MUST_HAVE_ZERO_CITY_MESHES")

    source_hashes = {}
    for name, source in SCRIPTS.items():
        if name in bpy.data.texts:
            raise RuntimeError("EXISTING_TEXT_MUST_NOT_BE_REPLACED:" + name)
        script = source.read_text(encoding="utf-8")
        bpy.data.texts.new(name).write(script)
        source_hashes[name] = hashlib.sha256(script.encode("utf-8")).hexdigest()

    note = bpy.data.texts.new("M37P2_WORKSPACE_READ_ME_FIRST_JA.txt")
    note.write(
        "G4-C7 M37-P2 — EDITABLE EMPTY ARTIST STUDIO, NOT ART.\\n"
        "No city geometry has been created. 3 cameras are PROVISIONAL.\\n"
        "In Blender Text Editor, run M37P2_RUN_ONCE_ENABLE_AUTHOR_REVIEW_PANEL.py\\n"
        "and M37P2_RUN_ONCE_PARALLEL_MACRO_LIVED_GUI.py once each.\\n"
        "Use P2 Author Views panel to split AERIAL + human-eye edit windows.\\n"
        "Both 3D views edit the SAME real scene; neither adds meshes.\\n"
        "Work on CITY MACRO and REAL MANUFACTURING/PUBLIC/RESEARCH/\\n"
        "CULTURE/HOUSING interior at the SAME TIME with actual GUI modelling.\\n"
        "NEVER reuse rejected M37-P1/O1/L/N forms or claim the empty file is ART.\\n"
        "Move cameras to meaningful positions after real 3D authoring.\\n"
        "Save As to a NEW .blend, NEVER overwrite this protected artifact.\\n"
        "Before review: ART HOLD, 331/993 NOT RUN, Minecraft FORBIDDEN.\\n"
        "No script in this file automatically runs on file open.\\n"
    )
    scene["P2_GUI_PACKAGE_STATUS"] = "EMPTY_DIRECT_AUTHOR_READY_NOT_ART"
    scene["P2_GUI_PACKAGE_INCLUDES_PARALLEL_AUTHOR_VIEWS"] = True
    scene["P2_GUI_PACKAGE_INCLUDES_EARLY_REVIEW_REFERENCE"] = True
    scene["P2_CITY_MESH_COUNT"] = 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT.resolve()), compress=False)

    if hash_file(ORIGINAL) != ORIGINAL_SHA256:
        raise RuntimeError("ORIGINAL_CHANGED_DURING_PACKAGING")
    manifest = {
        "schema": "g4c7-m37p2-integrated-empty-artist-native-workspace-v1",
        "result": "SAVED_NATIVE_EMPTY_EDITOR_STUDIO_NOT_ART",
        "source": str(ORIGINAL),
        "source_sha256": ORIGINAL_SHA256,
        "output": str(OUTPUT),
        "output_sha256": hash_file(OUTPUT),
        "output_bytes": OUTPUT.stat().st_size,
        "embedded_source_sha256": source_hashes,
        "real_city_meshes": 0,
        "cameras": 3,
        "city_art": "NOT_CREATED",
        "official_adoptions": 0,
        "formal_331_993": "NOT_RUN",
        "G0_S1_G1_G2_G3": "NOT_RUN",
        "MakeCode": "NOT_EVALUATED",
        "Minecraft": "FORBIDDEN",
        "gui_dual_view_in_real_desktop": "NOT_TESTED",
    }
    (ARTIFACT / "M37P2_WORKSPACE_BUILD_MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--build" not in sys.argv:
        raise SystemExit("Must specify --build. This only embeds editor scripts in an EMPTY .blend.")
    build()
