#!/usr/bin/env python3
"""G4-C7 M37-P2 append-only v3 correctness patch for the real native Blender editor.

The v2 Blender file is immutable. This updates ONLY two embedded Python Text
blocks in a NEW empty v3 .blend to incorporate independently tested fixes.
No meshes, visual art, image renderer runs, world writes or QA certification.
"""
import hashlib
import json
from pathlib import Path

V2=Path("artifacts/g4c7-m37p2-standalone-artist-workspace-v2-NOT-ART/M37P2_SINGLE_FILE_DIRECT_AUTHOR_AND_REVIEW_NOT_ART.blend")
V2_SHA="a772fc0bc1d1d2b23a33a14154ca5bcd08fcb1ced05ea5c9eb009aa02b19f99e"
OUTPUT=Path("artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend")
REPLACE={
    "M37P2_NATIVE_THREE_CAMERA_EARLY_REVIEW_NOT_ART.py":
        Path("tools/g4c7_m37p2_author_native_early_review.py"),
    "M37P2_RUN_ONCE_NATIVE_REVIEW_BUTTON.py":
        Path("tools/g4c7_m37p2_one_file_early_art_review_gui.py"),
}

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as stream:
        for piece in iter(lambda:stream.read(1048576),b""):
            h.update(piece)
    return h.hexdigest()

def main():
    import bpy
    if OUTPUT.exists():
        raise RuntimeError("V3_APPEND_ONLY_SOURCE_ALREADY_EXISTS")
    if not V2.is_file() or sha256(V2)!=V2_SHA:
        raise RuntimeError("IMMUTABLE_V2_SOURCE_WRONG_OR_MISSING")
    bpy.ops.wm.open_mainfile(filepath=str(V2.resolve()))
    scene=bpy.context.scene
    immutable={
        "P2_SOURCE_KIND":"UNAUTHORED_EMPTY_TEMPLATE",
        "P2_ART":"HOLD",
        "P2_OFFICIAL_ADOPTIONS":0,
        "P2_MINECRAFT":"FORBIDDEN",
        "P2_FORMAL_331_993":"NOT_RUN",
        "P2_STUDIO_STAGE":"EMPTY_NO_ART_CREATED",
        "P2_MAKECODE_COST":"NOT_EVALUATED",
    }
    for k,v in immutable.items():
        if scene.get(k)!=v:
            raise RuntimeError("INVALID_SCENE_CHARTER:"+k)
    if any(ob.type=="MESH" for ob in scene.objects):
        raise RuntimeError("MESH_IN_EMPTY_AUTHOR_EDITOR")
    if sum(ob.type=="CAMERA" for ob in scene.objects)!=3:
        raise RuntimeError("REQUIRED_THREE_CAMERAS_MISSING")
    hashes={}
    for name,path in REPLACE.items():
        source=path.read_text(encoding="utf-8")
        block=bpy.data.texts.get(name)
        if block is None:
            raise RuntimeError("EMBEDDED_P2_SCRIPT_MISSING:"+name)
        block.clear()
        block.write(source)
        hashes[name]=hashlib.sha256(source.encode("utf-8")).hexdigest()
    # Confirm the *source-code* fixes independently proven by CI 41428422529.
    assert "ob.name in coll.all_objects" in bpy.data.texts[
        "M37P2_NATIVE_THREE_CAMERA_EARLY_REVIEW_NOT_ART.py"].as_string()
    assert "bpy.data.is_dirty and not bpy.app.background" in bpy.data.texts[
        "M37P2_RUN_ONCE_NATIVE_REVIEW_BUTTON.py"].as_string()
    scene["P2_V3_EDITOR_FIX"]="BLENDER_45_COLLECTION_AND_HEADLESS_DIRTY_GUARD"
    scene["P2_V3_POSITIVE_NATIVE_THREE_VIEW_SMOKE"]="CI_41428422529_SUCCESS_EPHEMERAL_TETRA_ONLY"
    scene["P2_V3_GUI_REAL_AUTHOR_SCENE"]="NOT_TESTED_NO_ART"
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT.resolve()),compress=False)
    if sha256(V2)!=V2_SHA:
        raise RuntimeError("V2_IMMUTABLE_PARENT_CHANGED")
    report={
        "schema":"g4c7-m37p2-native-author-editor-patch-v3-v1",
        "result":"REAL_NATIVE_EMPTY_EDITOR_V3_PATCH_SAVED_NOT_ART",
        "source_v2_sha256":V2_SHA,
        "output_sha256":sha256(OUTPUT),
        "output_bytes":OUTPUT.stat().st_size,
        "embedded_patched_source_sha256":hashes,
        "positive_three_view_technical_smoke":"CI_41428422529_SUCCESS_EPHEMERAL_ONLY",
        "real_city_meshes":0,
        "new_city_art":"NOT_CREATED",
        "human_visual_review":"NOT_RUN",
        "ART":"HOLD",
        "adoptions":0,
        "formal_331_993":"NOT_RUN",
        "G0_S1_G1_G2_G3":"NOT_RUN",
        "MakeCode":"NOT_EVALUATED",
        "Minecraft":"FORBIDDEN",
        "main":"UNTOUCHED",
    }
    (OUTPUT.parent/"M37P2_V3_PATCH_MANIFEST.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__":
    main()
