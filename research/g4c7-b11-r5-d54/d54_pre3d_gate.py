"""D54 PRE-3D independent numeric design feasibility gate.

Reads author-authored JSON; no Blender/VTK/trimesh, and never claims that empty
space envelopes are completed rooms, collision-free GLBs or approved art.
"""
import copy
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def ellipsoid_value(p, scene):
    return sum(((p[i] - scene["void_center"][i]) /
                scene["void_radii"][i]) ** 2 for i in range(3))

def centerline_overlap(a, b):
    """Find a certified common interior sample of two convex ellipsoids."""
    worst_best = 999.0
    for i in range(1001):
        t = i / 1000
        p = [(1 - t) * a["void_center"][k] + t * b["void_center"][k]
             for k in range(3)]
        worst_best = min(worst_best, max(ellipsoid_value(p, a),
                                         ellipsoid_value(p, b)))
    return worst_best

def inspect(design):
    scenes = design["scenes"]
    names = [s["id"] for s in scenes]
    assert names == ["arrival", "maker", "research", "living"], names
    by_id = {s["id"]: s for s in scenes}
    assert len(by_id) == 4
    rise = design["tread_rise"]
    run = design["tread_run"]
    width = design["width"]
    assert 0.0 < rise <= 0.2 and 0.25 <= run <= 0.35
    assert width >= 2.8 and design["headroom_sample"] >= 2.15
    for s in scenes:
        assert all(r > 0 for r in s["void_radii"])
        eye = [s["foot"][0], s["foot"][1], s["foot"][2] + 1.65]
        assert ellipsoid_value(eye, s) < 1.0, (s["id"], "eye outside void")
    overlaps = {}
    for a, b in zip(scenes, scenes[1:]):
        value = centerline_overlap(a, b)
        assert value < 1.0, (a["id"], b["id"], "voids disconnected", value)
        overlaps[a["id"] + "->" + b["id"]] = round(value, 5)
    worst_value = 0.0
    n_samples = 0
    stair_count = 0
    legs = design["legs"]
    assert len(legs) == 3
    for leg in legs:
        start, end = by_id[leg["start"]], by_id[leg["end"]]
        count = leg["stairs"]
        assert isinstance(count, int) and count > 0
        stair_count += count
        p0, p1 = start["foot"], end["foot"]
        actual_rise = p1[2] - p0[2]
        assert abs(actual_rise - count * rise) < 1e-7, (leg, "landing mismatch")
        dx, dy = p1[0]-p0[0], p1[1]-p0[1]
        distance = math.hypot(dx, dy)
        stair_run = count * run
        flat = (distance - stair_run) / 2
        assert flat >= 1.5, (leg, "insufficient flat approach/landing")
        normal = [-dy / distance, dx / distance]
        for i in range(301):
            t = i / 300
            s = t * distance
            progress = max(0, min(1, (s - flat) / stair_run))
            z = p0[2] + progress * actual_rise
            for side in (-width/2, 0, width/2):
                for height in (0.15, 1.7, design["headroom_sample"]):
                    point = [p0[0] + t*dx + normal[0]*side,
                             p0[1] + t*dy + normal[1]*side,
                             z + height]
                    value = min(ellipsoid_value(point, sc) for sc in scenes)
                    worst_value = max(worst_value, value)
                    n_samples += 1
                    assert value <= 1.0 + 1e-9, (leg, "reserved route section exits voids", point, value)
    assert stair_count == 120
    return {"route_footprint_and_head_samples": n_samples,
            "overlap_worst_ellipsoid_scores": overlaps,
            "max_path_void_score": round(worst_value, 5),
            "stair_design_count": stair_count,
            "claims":"Only PRE-3D reserved empty volume, step-height arithmetic and sampled route cross sections"}

def main():
    design = json.loads((ROOT / "d54_spatial_contract.json").read_text(encoding="utf-8"))
    out = inspect(design)
    # Mutate inputs intentionally to establish that the gate can catch clear mistakes.
    bad_landing = copy.deepcopy(design)
    bad_landing["scenes"][-1]["foot"][2] += 0.34
    try:
        inspect(bad_landing)
    except AssertionError:
        out["negative_landing_disconnection_detected"] = True
    else:
        raise RuntimeError("Broken landing was not detected")
    bad_void = copy.deepcopy(design)
    bad_void["scenes"][0]["void_radii"][1] = 7
    try:
        inspect(bad_void)
    except AssertionError:
        out["negative_void_narrowing_detected"] = True
    else:
        raise RuntimeError("Artificially narrowed arrival void was not detected")
    out["art"] = "NOT JUDGED"
    out["true3d"] = "NOT RUN"
    out["official_331_993"] = "NOT RUN"
    out["formal_G0_S1_G1_G2_G3"] = "NOT RUN"
    out["construction"] = "FORBIDDEN"
    path = ROOT / "d54_pre3d_audit.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
