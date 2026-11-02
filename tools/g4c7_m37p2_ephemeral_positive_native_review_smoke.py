#!/usr/bin/env python3
"""EPHEMERAL bpy test harness, NEVER a G4-C7 art generator or proposal.

Purely temporary FIVE tetrahedra test the otherwise untested POSITIVE path
of the artist-native single-file early review. This is not city design; it is
not saved to GitHub, and is always deleted in a TemporaryDirectory.

Run by CI only, with native Blender bpy. No Minecraft / MakeCode access.
"""
import hashlib
import json
import os
from pathlib import Path
import tempfile

ART_SOURCE = Path(
    "artifacts/g4c7-m37p2-standalone-artist-workspace-v2-NOT-ART"
    "/M37P2_SINGLE_FILE_DIRECT_AUTHOR_AND_REVIEW_NOT_ART.blend"
)
PIN_SHA256 = "a772fc0bc1d1d2b23a33a14154ca5bcd08fcb1ced05ea5c9eb009aa02b19f99e"
GROUPS = (
    "P2_CITY_MACRO_DIRECT_AUTHOR",
    "P2_INHABITED_SECTION_DIRECT_AUTHOR",
    "P2_PUBLIC_FACTORY_BOUNDARY_DIRECT_AUTHOR",
    "P2_RESEARCH_CULTURE_DIRECT_AUTHOR",
    "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
)
CAMERAS = {
    "P2_CAMERA_AERIAL": ((36, -55, 37), (0, 0, 0)),
    "P2_CAMERA_PUBLIC_EYE": ((-34, -44, 11), (0, 0, 0)),
    "P2_CAMERA_HABITAT_EYE": ((-33, 24, 12), (0, 0, 0)),
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def make_test_tetra(bpy, col, idx):
    """Deliberately tiny diagnostic tetra, NOT reusable G4-C7 building geometry."""
    mesh = bpy.data.meshes.new("CI_ONLY_NO_ART_TETRA_" + str(idx))
    mesh.from_pydata(
        [(idx * 4 - 8, 0.0, 0.0), (idx * 4 - 5, 0.0, 0.0),
         (idx * 4 - 6, 2.0, 0.0), (idx * 4 - 6, 1.0, 6.0)],
        [], [(0, 2, 1), (0, 1, 3), (1, 2, 3), (2, 0, 3)],
    )
    mesh.update()
    obj = bpy.data.objects.new("CI_ONLY_EPHEMERAL_NOT_CITY_%d" % idx, mesh)
    col.objects.link(obj)
    return obj


def main():
    import bpy
    from mathutils import Vector

    if os.environ.get("CI") != "true" or not bpy.app.background:
        raise RuntimeError("EPHEMERAL_FIXTURE_MAY_RUN_ONLY_IN_HEADLESS_GITHUB_CI")
    if not ART_SOURCE.is_file() or sha256(ART_SOURCE) != PIN_SHA256:
        raise RuntimeError("UNEXPECTED_ARTIST_MASTER_SHA256")
    with tempfile.TemporaryDirectory(prefix="g4c7-p2-NO-ART-test-") as directory:
        tmp = Path(directory)
        bpy.ops.wm.open_mainfile(filepath=str(ART_SOURCE.resolve()))
        scene = bpy.context.scene
        if any(obj.type == "MESH" for obj in scene.objects):
            raise RuntimeError("IMMUTABLE_ORIGINAL_MUST_BE_EMPTY")
        for idx, name in enumerate(GROUPS):
            make_test_tetra(bpy, bpy.data.collections[name], idx)
        for name, (position, target) in CAMERAS.items():
            cam = scene.objects[name]
            cam.location = position
            cam.rotation_euler = (
                Vector(target) - cam.location
            ).to_track_quat("-Z", "Y").to_euler()
        # Restore visibly illuminated triangles without creating any G4-C7 art.
        light = bpy.data.lights.new("CI_EPHEMERAL_LIGHT_NOT_ART", "AREA")
        light.energy = 2500
        light_obj = bpy.data.objects.new("CI_EPHEMERAL_LIGHT_NOT_ART", light)
        scene.collection.objects.link(light_obj)
        light_obj.location = (0.0, -5.0, 30.0)
        scene.world.use_nodes = True
        scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 1.0
        scene["P2_CAMERA_VIEWS_AUTHOR_APPROVED"] = True
        scene["P2_SOURCE_KIND"] = "DIRECT_EDITOR_AUTHORED_NATIVE_3D"
        scene["P2_STUDIO_STAGE"] = "DIRECT_AUTHOR_SUBMITTED_FOR_EARLY_ART_REVIEW_NOT_PASSED"
        scene["P2_ART"] = "HOLD"
        scene["P2_OFFICIAL_ADOPTIONS"] = 0
        scene["P2_MINECRAFT"] = "FORBIDDEN"
        # This temporary CI declaration is a test input, NOT author provenance.
        scene["P2_CI_TEMPORARY_FIXTURE_NOT_ART"] = True
        master = tmp / "M37P2_POSITIVE_CI_TEST_FIXTURE_NEVER_ART.blend"
        bpy.ops.wm.save_as_mainfile(filepath=str(master), compress=False)

        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.wm.open_mainfile(filepath=str(master.resolve()))
        if any(o.type == "MESH" for o in bpy.context.scene.objects) is False:
            raise RuntimeError("TEMP_FIXTURE_DID_NOT_SURVIVE_REOPEN")
        source = bpy.data.texts["M37P2_RUN_ONCE_NATIVE_REVIEW_BUTTON.py"].as_string()
        scope = {"__name__": "g4c7_p2_test_ui_module",
                 "__file__": str(tmp / "EMBEDDED_ONLY_NO_DISK_SCRIPT.py")}
        exec(compile(source, "M37P2_RUN_ONCE_NATIVE_REVIEW_BUTTON.py", "exec"), scope)
        # Test the same entrypoint as the GUI button, without fake GUI clicks.
        output_dir = tmp / "REAL_THREE_IMAGE_SMOKE_NOT_ART"
        print("P2_EPHEMERAL_POSITIVE_REVIEW_START", flush=True)
        result = scope["run_review"](str(output_dir))
        if result != output_dir:
            raise RuntimeError("GUI_WRAPPER_DESTINATION_MISMATCH")
        manifest = json.loads(
            (output_dir / "M37P2_EARLY_REVIEW_UNAPPROVED_MANIFEST.json").read_text()
        )
        if set(manifest["early_native_three_view_renders"]) != {
            "AERIAL", "PUBLIC_EYE", "HABITAT_EYE"
        }:
            raise RuntimeError("THREE_REAL_CAMERA_RENDERS_NOT_COMPLETED")
        image_sha = {}
        for key, info in manifest["early_native_three_view_renders"].items():
            image_path = output_dir / info["name"]
            if not image_path.read_bytes().startswith(bytes((137, 80, 78, 71, 13, 10, 26, 10))):
                raise RuntimeError("INVALID_REAL_PNG:" + key)
            if sha256(image_path) != info["sha256"]:
                raise RuntimeError("RENDER_SHA_MISMATCH:" + key)
            image_sha[key] = info["sha256"]
        if manifest["official_adoption"] != 0 or manifest["Minecraft"] != "FORBIDDEN":
            raise RuntimeError("ILLEGAL_ART_OR_WORLD_PROMOTION")
        if sha256(master) != manifest["source_sha256_before_and_after"]:
            raise RuntimeError("ARTIST_MASTER_WAS_MODIFIED_BY_REVIEW")
        if sha256(ART_SOURCE) != PIN_SHA256:
            raise RuntimeError("IMMUTABLE_GITHUB_NATIVE_MASTER_CHANGED")
        print(json.dumps({
            "result": "PASS_EPHEMERAL_TECH_POSITIVE_REVIEW_ONLY",
            "images_rendered_from_reopened_native_blend": len(image_sha),
            "camera_image_sha256": image_sha,
            "native_author_art": "NOT_CREATED_CI_TETRA_ONLY",
            "temporary_output": "DELETED_ON_SUCCESS",
            "ART": "HOLD",
            "adoption": 0,
            "formal_safety": "NOT_RUN",
            "Minecraft": "FORBIDDEN"
        }, indent=2), flush=True)


if __name__ == "__main__":
    main()
