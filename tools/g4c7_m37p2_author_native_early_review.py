#!/usr/bin/env python3
"""G4-C7 M37-P2: inspect an existing DIRECTLY authored Blender master.

NO geometry generation. All city meshes must already be directly authored in
Blender. Does not reuse the rejected P1 patch/wall/bridge native city.
The three real review images still require human absolute ART judgment.

blender -b /path/to/P2_DIRECT_AUTHOR_MASTER.blend --python \
  tools/g4c7_m37p2_author_native_early_review.py -- --out /path/to/review
python tools/g4c7_m37p2_author_native_early_review.py --self-test
This tool never saves/modifies the source .blend or writes a Minecraft world.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

CAMERAS = {
    "AERIAL": "P2_CAMERA_AERIAL",
    "PUBLIC_EYE": "P2_CAMERA_PUBLIC_EYE",
    "HABITAT_EYE": "P2_CAMERA_HABITAT_EYE",
}

# Original empty studio camera positions; these are provisional, NOT proof of
# actual city viewpoints. Reject a click-through approval on an unedited rig.
PROVISIONAL_CAMERA_LOCATIONS = {
    "P2_CAMERA_AERIAL": (190.0, -165.0, 132.0),
    "P2_CAMERA_PUBLIC_EYE": (-84.0, -78.0, 12.0),
    "P2_CAMERA_HABITAT_EYE": (-62.0, 50.0, 22.0),
}


def unchanged_template_viewpoints(poses, minimum_move=1.0):
    """Pure geometric preflight; does not decide artistic quality."""
    stale = []
    for name, initial in PROVISIONAL_CAMERA_LOCATIONS.items():
        point = poses.get(name)
        if point is None or len(point) != 3:
            stale.append(name)
            continue
        move_squared = sum((float(a) - b) ** 2 for a, b in zip(point, initial))
        if move_squared < minimum_move ** 2:
            stale.append(name)
    return sorted(stale)



def check_review_contract(meta, camera_names, mesh_count):
    """Fail closed: metadata is a declaration, NOT proof of author provenance."""
    errors = []
    required = {
        "P2_SOURCE_KIND": "DIRECT_EDITOR_AUTHORED_NATIVE_3D",
        "P2_PARENT_REJECTED_FORM_IMPORTED": 0,
        "P2_ART": "HOLD",
        "P2_OFFICIAL_ADOPTIONS": 0,
        "P2_MINECRAFT": "FORBIDDEN",
        "P2_FORMAL_331_993": "NOT_RUN",
        "P2_MAKECODE_COST": "NOT_EVALUATED",
        "P2_CAMERA_VIEWS_AUTHOR_APPROVED": True,
        "P2_STUDIO_STAGE": "DIRECT_AUTHOR_SUBMITTED_FOR_EARLY_ART_REVIEW_NOT_PASSED",
    }
    for key, value in required.items():
        if meta.get(key) != value:
            errors.append("INVALID_SOURCE_CHARTER:" + key)
    if not isinstance(mesh_count, int) or mesh_count < 1:
        errors.append("NO_REAL_MESH_GEOMETRY")
    missing = set(CAMERAS.values()) - set(camera_names)
    if missing:
        errors.append("MISSING_FIXED_NATIVE_CAMERAS:" + ",".join(sorted(missing)))
    return errors


def self_test():
    meta = {
        "P2_SOURCE_KIND": "DIRECT_EDITOR_AUTHORED_NATIVE_3D",
        "P2_PARENT_REJECTED_FORM_IMPORTED": 0,
        "P2_ART": "HOLD",
        "P2_OFFICIAL_ADOPTIONS": 0,
        "P2_MINECRAFT": "FORBIDDEN",
        "P2_FORMAL_331_993": "NOT_RUN",
        "P2_MAKECODE_COST": "NOT_EVALUATED",
        "P2_CAMERA_VIEWS_AUTHOR_APPROVED": True,
        "P2_STUDIO_STAGE": "DIRECT_AUTHOR_SUBMITTED_FOR_EARLY_ART_REVIEW_NOT_PASSED",
    }
    assert not check_review_contract(meta, tuple(CAMERAS.values()), 1)
    negatives = [
        ("false_art_pass", {"P2_ART": "PASS"}),
        ("false_adoption", {"P2_OFFICIAL_ADOPTIONS": 1}),
        ("unsafe_minecraft", {"P2_MINECRAFT": "ALLOWED"}),
        ("false_safety", {"P2_FORMAL_331_993": "PASS"}),
        ("fake_makecode", {"P2_MAKECODE_COST": "PASS"}),
        ("recycled_old_3d", {"P2_PARENT_REJECTED_FORM_IMPORTED": 1}),
        ("no_provenance_declaration", {"P2_SOURCE_KIND": "PROCEDURAL_PATCH_BRIDGE"}),
    ]
    for label, change in negatives:
        assert check_review_contract(dict(meta, **change), tuple(CAMERAS.values()), 1), label
    assert check_review_contract(meta, (), 1)
    assert check_review_contract(meta, tuple(CAMERAS.values()), 0)
    assert unchanged_template_viewpoints(PROVISIONAL_CAMERA_LOCATIONS) == sorted(CAMERAS.values())
    moved = {name: (p[0] + 5.0, p[1] + 2.0, p[2] + 1.0)
             for name, p in PROVISIONAL_CAMERA_LOCATIONS.items()}
    assert unchanged_template_viewpoints(moved) == []
    moved["P2_CAMERA_PUBLIC_EYE"] = PROVISIONAL_CAMERA_LOCATIONS["P2_CAMERA_PUBLIC_EYE"]
    assert unchanged_template_viewpoints(moved) == ["P2_CAMERA_PUBLIC_EYE"]
    return {
        "result": "PASS_INVARIANT_AND_NEGATIVE_TESTS_ONLY",
        "negative_controls": len(negatives) + 3,
        "camera_template_pose_negative": "EXPECTED_UNEDITED_VIEWPOINTS_REJECTED",
        "new_blend_art": "NOT_CREATED_BY_THIS_TOOL",
        "absolute_art": "HUMAN_REVIEW_REQUIRED",
        "Minecraft": "FORBIDDEN",
    }


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def embedded_cameras(scene):
    """Reuse prior P2 closed-solid negative-control implementation."""
    spec = importlib.util.spec_from_file_location(
        "p2_camera_audit",
        Path(__file__).with_name("g4c7_m37p2_native_camera_inside_solid_audit.py"),
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import bpy

    depsgraph = bpy.context.evaluated_depsgraph_get()
    targets = [scene.objects[name] for name in CAMERAS.values()]
    points = [tuple(ob.matrix_world.translation) for ob in targets]
    issues = {ob.name: [] for ob in targets}
    open_meshes = []
    for ob in scene.objects:
        if ob.type != "MESH":
            continue
        evaluated = ob.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        try:
            faces = [tuple(poly.vertices) for poly in mesh.polygons]
            if not mod.closed_faces(faces):
                open_meshes.append(ob.name)
                continue
            bounds_min = [
                min((evaluated.matrix_world @ v.co)[i] for v in mesh.vertices)
                for i in range(3)
            ]
            bounds_max = [
                max((evaluated.matrix_world @ v.co)[i] for v in mesh.vertices)
                for i in range(3)
            ]
            candidate = [
                i for i, p in enumerate(points)
                if all(bounds_min[k] <= p[k] <= bounds_max[k] for k in range(3))
            ]
            if not candidate:
                continue
            mesh.calc_loop_triangles()
            verts = [tuple(evaluated.matrix_world @ v.co) for v in mesh.vertices]
            triangles = [tuple(t.vertices) for t in mesh.loop_triangles]
            for i in candidate:
                if mod.point_inside_closed_mesh(points[i], verts, faces, triangles):
                    issues[targets[i].name].append(ob.name)
        finally:
            evaluated.to_mesh_clear()
    return {k: v for k, v in issues.items() if v}, open_meshes


def native_review(output_dir):
    import bpy

    blend = Path(bpy.data.filepath)
    if not blend.is_file() or blend.suffix.lower() != ".blend":
        raise RuntimeError("EXISTING_SAVED_NATIVE_BLEND_REQUIRED")
    source_sha_before = sha256(blend)
    rejected_native_sha256 = {
        "ca402f8e58269535bd6838cc8e5201000e9bc137dc578f0751f76bcb0d3b262d",
        "7845343514b79067835ddbbd18aabf93439a391f4a2c0983227475b18331b2f1",
        "0817bf8a9681e9380b8167e75ddc236dbcab18920b01298c5e405ed46752bdff",
    }
    if source_sha_before in rejected_native_sha256:
        raise RuntimeError("PREVIOUSLY_REJECTED_NATIVE_SOURCE_CANNOT_BE_P2")
    scene = bpy.context.scene
    keys = (
        "P2_SOURCE_KIND", "P2_PARENT_REJECTED_FORM_IMPORTED", "P2_ART",
        "P2_OFFICIAL_ADOPTIONS", "P2_MINECRAFT", "P2_FORMAL_331_993",
        "P2_MAKECODE_COST", "P2_CAMERA_VIEWS_AUTHOR_APPROVED",
        "P2_STUDIO_STAGE",
    )
    metadata = {key: scene.get(key) for key in keys}
    meshes = [
        ob for ob in scene.objects
        if ob.type == "MESH" and len(ob.data.vertices) > 0
    ]
    cams = [ob.name for ob in scene.objects if ob.type == "CAMERA"]
    errors = check_review_contract(metadata, cams, len(meshes))
    if errors:
        raise RuntimeError("P2_REVIEW_INPUT_REJECTED:" + ",".join(errors))
    required_collections = (
        "P2_CITY_MACRO_DIRECT_AUTHOR",
        "P2_INHABITED_SECTION_DIRECT_AUTHOR",
        "P2_PUBLIC_FACTORY_BOUNDARY_DIRECT_AUTHOR",
        "P2_RESEARCH_CULTURE_DIRECT_AUTHOR",
        "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
    )
    for name in required_collections:
        coll = bpy.data.collections.get(name)
        if coll is None or not any(ob in coll.all_objects and ob in meshes for ob in scene.objects):
            raise RuntimeError("NO_ACTUAL_DIRECT_AUTHOR_MESH_IN_AREA:" + name)
    all_names = {
        ob.name for name in required_collections
        for ob in bpy.data.collections[name].all_objects if ob.type == "MESH"
    }
    if len(all_names) < 5:
        raise RuntimeError("ONLY_TRIVIAL_OR_DUPLICATE_AUTHOR_CONTENT")
    if "m37p1" in blend.name.lower() or "m37o" in blend.name.lower():
        raise RuntimeError("REJECTED_OLD_ART_NOT_ALLOWED_AS_P2_MASTER")
    rejected_prefixes = ("M37P1_", "M37O_", "M37L_", "M37N_")
    if any(ob.name.startswith(rejected_prefixes) for ob in meshes):
        raise RuntimeError("REJECTED_OLD_MESH_NAMES_PRESENT_IN_AUTHOR_MASTER")
    camera_positions = {
        name: tuple(scene.objects[name].matrix_world.translation)
        for name in CAMERAS.values()
    }
    unchanged = unchanged_template_viewpoints(camera_positions)
    if unchanged:
        raise RuntimeError("CAMERA_APPROVAL_WITH_UNEDITED_TEMPLATE_RIG:" +
                           ",".join(unchanged))
    issues, nonwatertight = embedded_cameras(scene)
    if issues:
        raise RuntimeError("CAMERA_EMBEDDED_IN_CLOSED_MESH:" + json.dumps(issues))

    output = Path(output_dir).resolve()
    if output == blend.parent.resolve() or blend.is_relative_to(output):
        raise RuntimeError("REVIEW_OUTPUT_MUST_NOT_OVERWRITE_AUTHOR_MASTER")
    if output.exists() and any(output.iterdir()):
        raise RuntimeError("REVIEW_OUTPUT_MUST_BE_NEW_OR_EMPTY_APPEND_ONLY")
    output.mkdir(parents=True, exist_ok=True)
    # Review camera and render settings are RAM-only: no save_as_mainfile.
    original_camera, original_path = scene.camera, scene.render.filepath
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 24
    scene.render.image_settings.file_format = "PNG"
    scene.render.resolution_x = 960
    scene.render.resolution_y = 600
    scene.render.resolution_percentage = 100
    images = {}
    try:
        for key, name in CAMERAS.items():
            scene.camera = scene.objects[name]
            image_path = output / ("M37P2_" + key + ".png")
            scene.render.filepath = str(image_path)
            bpy.ops.render.render(write_still=True)
            images[key] = {"name": image_path.name, "sha256": sha256(image_path)}
    finally:
        scene.camera = original_camera
        scene.render.filepath = original_path
    if sha256(blend) != source_sha_before:
        raise RuntimeError("AUTHOR_SOURCE_CHANGED_DURING_REVIEW")
    report = {
        "schema": "g4c7-m37p2-artist-native-early-review-v1",
        "source_blend": blend.name,
        "source_sha256_before_and_after": source_sha_before,
        "declared_provenance_not_independently_verified": metadata,
        "saved_scene_mesh_objects": len(meshes),
        "early_native_three_view_renders": images,
        "camera_embedded_in_closed_solid": issues,
        "unproven_open_mesh_objects": nonwatertight,
        "absolute_art": "NOT_ASSESSED_HUMAN_ABSOLUTE_REVIEW_REQUIRED",
        "inhabited_city_and_public_work_life": "NOT_CERTIFIED",
        "official_adoption": 0,
        "formal_331_993": "NOT_RUN",
        "G0_S1_G1_G2_G3": "NOT_RUN",
        "MakeCode": "NOT_EVALUATED",
        "Minecraft": "FORBIDDEN",
        "limitations": "Provenance labels and three image hashes are not evidence of artistic quality.",
    }
    (output / "M37P2_EARLY_REVIEW_UNAPPROVED_MANIFEST.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args(
        sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    )
    if args.self_test:
        print(json.dumps(self_test(), ensure_ascii=False, indent=2))
    else:
        if not args.out:
            parser.error("--out required for existing directly authored Blender master")
        native_review(args.out)
