#!/usr/bin/env python3
"""M37-P2 auxiliary preflight: identify saved Blender cameras embedded in closed solids.

Usage:
  python tools/g4c7_m37p2_native_camera_inside_solid_audit.py --self-test
  blender -b ARTIST_AUTHORED.blend --python tools/g4c7_m37p2_native_camera_inside_solid_audit.py -- --audit

This does NOT create art, judge ART, validate paths/support, run 331/993 or authorize
Minecraft/MakeCode operations. It does not move cameras or alter saved Blender objects.
"""
import json
import math
import sys
from collections import Counter

RAYS = ((1.0, 0.271, 0.123), (0.193, 1.0, 0.337), (0.211, 0.371, 1.0))
EPS = 1.0e-7


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def ray_triangle_distance(origin, ray, a, b, c):
    e1, e2 = sub(b, a), sub(c, a)
    h = cross(ray, e2)
    det = dot(e1, h)
    if abs(det) < EPS:
        return None
    inv = 1.0 / det
    s = sub(origin, a)
    u = inv * dot(s, h)
    if u < -EPS or u > 1.0 + EPS:
        return None
    q = cross(s, e1)
    v = inv * dot(ray, q)
    if v < -EPS or u + v > 1.0 + EPS:
        return None
    t = inv * dot(e2, q)
    return t if t > EPS else None


def closed_faces(faces):
    edges = Counter()
    for f in faces:
        if len(f) < 3:
            return False
        for a, b in zip(f, f[1:] + f[:1]):
            edges[tuple(sorted((a, b)))] += 1
    return bool(edges) and all(n == 2 for n in edges.values())


def point_inside_closed_mesh(point, verts, faces, triangles):
    if not closed_faces(faces):
        return None  # open surfaces cannot give a trustworthy solid verdict
    for axis in range(3):
        coords = [v[axis] for v in verts]
        if not min(coords) + EPS < point[axis] < max(coords) - EPS:
            return False
    votes = []
    for ray in RAYS:
        distances = sorted(t for i, j, k in triangles
                           if (t := ray_triangle_distance(point, ray,
                                                          verts[i], verts[j], verts[k])) is not None)
        unique = []
        for t in distances:
            if not unique or abs(t - unique[-1]) > 1.0e-5:
                unique.append(t)
        votes.append(len(unique) % 2 == 1)
    return True if sum(votes) >= 2 else False


def test_p1_research_camera_case():
    # Exact M37-P1 source coordinates: EAST_RESEARCH_MAKER_WING and RESEARCH_EYE.
    ax, ay = 54.0, -69.0
    bx, by = 41.0, 0.0
    thickness, z0, z1 = 3.5, 3.0, 62.0
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    nx, ny = -dy / length * thickness / 2, dx / length * thickness / 2
    verts = [(ax+nx, ay+ny, z0), (bx+nx, by+ny, z0),
             (bx-nx, by-ny, z0), (ax-nx, ay-ny, z0),
             (ax+nx, ay+ny, z1), (bx+nx, by+ny, z1),
             (bx-nx, by-ny, z1), (ax-nx, ay-ny, z1)]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4),
             (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    triangles = [(f[0], f[i], f[i+1]) for f in faces
                 for i in range(1, len(f)-1)]
    inside = point_inside_closed_mesh((40.0, -3.0, 37.0), verts, faces, triangles)
    assert inside is True, "P1 black RESEARCH_EYE embedded in wing must be detected"
    assert point_inside_closed_mesh((0.0, -3.0, 37.0), verts, faces, triangles) is False
    u = ((40-ax)*dx + (-3-ay)*dy) / (length*length)
    distance = math.hypot(40-(ax+u*dx), -3-(ay+u*dy))
    assert abs(distance - 1.5381556881188876) < 1e-7
    return {"P1_RESEARCH_EYE": "INSIDE_EAST_RESEARCH_MAKER_WING",
            "wall_axis_distance": round(distance, 6),
            "wall_half_thickness": thickness / 2,
            "result": "PASS_EXPECTED_DEFECT_DETECTED"}


def audit_blender_scene():
    import bpy  # Only Blender must import bpy; pure-Python regression works everywhere.
    dg = bpy.context.evaluated_depsgraph_get()
    cameras = [o for o in bpy.context.scene.objects if o.type == "CAMERA"]
    solids = []
    ignored = []
    for obj in bpy.context.scene.objects:
        if obj.type != "MESH":
            continue
        ev = obj.evaluated_get(dg)
        mesh = ev.to_mesh()
        try:
            faces = [tuple(p.vertices) for p in mesh.polygons]
            if not closed_faces(faces):
                ignored.append(obj.name)
                continue
            mesh.calc_loop_triangles()
            verts = [tuple(ev.matrix_world @ v.co) for v in mesh.vertices]
            triangles = [tuple(t.vertices) for t in mesh.loop_triangles]
            solids.append((obj.name, verts, faces, triangles))
        finally:
            ev.to_mesh_clear()
    issues = {}
    for cam in cameras:
        point = tuple(cam.matrix_world.translation)
        hits = [name for name, verts, faces, tris in solids
                if point_inside_closed_mesh(point, verts, faces, tris)]
        if hits:
            issues[cam.name] = hits
    report = {"tool": "m37p2-native-camera-inside-solid-audit-v1",
              "art": "NOT_EVALUATED", "safety_331_993": "NOT_RUN",
              "minecraft": "FORBIDDEN",
              "camera_count": len(cameras), "watertight_mesh_count": len(solids),
              "open_or_nonmanifold_mesh_count": len(ignored),
              "cameras_inside_closed_solid": issues,
              "pass": not bool(issues),
              "limitations": "No image-quality, line-of-sight, traversal or safety certification"}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if issues:
        raise SystemExit(2)


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        print(json.dumps(test_p1_research_camera_case(), indent=2))
    elif "--audit" in sys.argv:
        audit_blender_scene()
    else:
        raise SystemExit("Use --self-test (pure Python) or --audit (Blender).")
