#!/usr/bin/env python3
"""Create a NEW append-only genuine Blender workspace from the immutable v1.

This embeds the fixed GUI review operator, its pure camera-solid dependency,
and the revised native reviewer directly inside a separate .blend. No shape,
mesh, scene image, source art or Minecraft world write is created.
"""
import hashlib
import json
from pathlib import Path

OLD=Path("artifacts/g4c7-m37p2-integrated-native-author-workspace-NOT-ART/M37P2_INTEGRATED_EMPTY_ARTIST_WORKSPACE_NOT_ART.blend")
OLD_HASH="6ca727def08cce9220dbde59f5836248cb5d0def39c7f375c9308af1461ee904"
OUTPUT=Path("artifacts/g4c7-m37p2-standalone-artist-workspace-v2-NOT-ART/M37P2_SINGLE_FILE_DIRECT_AUTHOR_AND_REVIEW_NOT_ART.blend")
FILES={
    "M37P2_NATIVE_THREE_CAMERA_EARLY_REVIEW_NOT_ART.py":"tools/g4c7_m37p2_author_native_early_review.py",
    "M37P2_CAMERA_INSIDE_SOLID_AUDIT.py":"tools/g4c7_m37p2_native_camera_inside_solid_audit.py",
    "M37P2_RUN_ONCE_NATIVE_REVIEW_BUTTON.py":"tools/g4c7_m37p2_one_file_early_art_review_gui.py",
}

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as inp:
        for chunk in iter(lambda:inp.read(1<<20),b""):
            h.update(chunk)
    return h.hexdigest()

def build():
    import bpy
    if not OLD.is_file() or sha(OLD)!=OLD_HASH:
        raise RuntimeError("PINNED_PARENT_WORKSPACE_MISSING_OR_CHANGED")
    if OUTPUT.exists():
        raise RuntimeError("APPEND_ONLY_NEW_WORKSPACE_ALREADY_EXISTS")
    if not all(Path(p).is_file() for p in FILES.values()):
        raise RuntimeError("EMBEDDED_SCRIPT_SOURCE_MISSING")
    bpy.ops.wm.open_mainfile(filepath=str(OLD.resolve()))
    scene=bpy.context.scene
    required={"P2_SOURCE_KIND":"UNAUTHORED_EMPTY_TEMPLATE",
              "P2_ART":"HOLD","P2_OFFICIAL_ADOPTIONS":0,
              "P2_MINECRAFT":"FORBIDDEN","P2_FORMAL_331_993":"NOT_RUN",
              "P2_STUDIO_STAGE":"EMPTY_NO_ART_CREATED"}
    for key,expected in required.items():
        if scene.get(key)!=expected:
            raise RuntimeError("P2_WORKSPACE_SOURCE_NOT_EMPTY_OR_CHARTER_BAD:"+key)
    if any(ob.type=="MESH" for ob in scene.objects):
        raise RuntimeError("FORBIDDEN_GEO_IN_EMPTY_WORKSPACE")
    sha_sources={}
    for name,filename in FILES.items():
        source=Path(filename).read_text(encoding="utf-8")
        block=bpy.data.texts.get(name)
        if block is None:
            block=bpy.data.texts.new(name)
        else:
            # Replace embedded outdated review code only in THIS NEW v2 copy.
            block.clear()
        block.write(source)
        sha_sources[name]=hashlib.sha256(source.encode("utf-8")).hexdigest()
    doc=bpy.data.texts.new("M37P2_V2_NATIVE_GUI_REVIEW_INSTRUCTIONS_JA.txt")
    doc.write(
        "M37-P2 v2 new empty artist workspace. NO NEW CITY ART!\\n"
        "For REAL mesh authoring use the native Blender GUI and author-edit\\n"
        "city macro and inhabited section together in this scene.\\n"
        "Run existing M37P2_RUN_ONCE_ENABLE_AUTHOR_REVIEW_PANEL.py and\\n"
        "M37P2_RUN_ONCE_PARALLEL_MACRO_LIVED_GUI.py manually once.\\n"
        "NEW: run M37P2_RUN_ONCE_NATIVE_REVIEW_BUTTON.py once to register\\n"
        "the P2 Early Art Review sidebar action (does not auto-render).\\n"
        "Your real edited city must contain at least five distinct meshes in\\n"
        "the five source-author collections, not rejected M37-P1/O1/L/N forms.\\n"
        "Reposition all 3 camera objects, explicitly approve viewpoints.\\n"
        "Use author panel to mark source ready, then SAVE AS a NEW .blend,\\n"
        "close and reopen and re-register the native review GUI operator.\\n"
        "Hit 'Render 3 genuine views (ART UNAPPROVED)' to run full fail-closed\\n"
        "mesh/source/camera and actual three-view Cycles image checks.\\n"
        "NEVER run the embedded CLI source directly as a Blender Text Script.\\n"
        "Approval is ONLY to render candidate for independent visual review.\\n"
        "Never overwrite this v2 empty master. ART HOLD, 0 adoptions.\\n"
        "331/993 and G0/S1/G1/G2/G3 NOT RUN. Minecraft FORBIDDEN.\\n")
    scene["P2_V2_STANDALONE_GUI_EARLY_REVIEW"]="EMBEDDED_NOT_RUN_ART_HOLD"
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT.resolve()),compress=False)
    if sha(OLD)!=OLD_HASH:
        raise RuntimeError("PARENT_WORKSPACE_CHANGED")
    manifest={
        "schema":"g4c7-m37p2-self-contained-native-artist-workspace-v2",
        "result":"GENUINE_EMPTY_BLENDER_SOURCE_AND_GUI_RENDER_CONTROL_NOT_ART",
        "parent_sha256":OLD_HASH,
        "output":str(OUTPUT),
        "output_sha256":sha(OUTPUT),
        "bytes":OUTPUT.stat().st_size,
        "embedded_sources_sha256":sha_sources,
        "city_art":"NOT_CREATED",
        "real_city_meshes":0,
        "review_images":"NOT_RENDERED_NO_ART",
        "manual_blender_gui":"NOT_TESTED",
        "official_art_adoptions":0,
        "formal_331_993":"NOT_RUN",
        "G0_S1_G2_G3":"NOT_RUN",
        "Minecraft":"FORBIDDEN",
    }
    (OUTPUT.parent/"M37P2_V2_NATIVE_WORKSPACE_MANIFEST.json").write_text(
       json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=="__main__":
    build()
