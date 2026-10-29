"""D56-P2: independent PRE-3D reservation and access checks.
These tests inspect JSON *not any real geometry*. No source passing this gate
can be described as watertight, navigable, daylit, stable, or artistically accepted.
"""
from pathlib import Path
import copy, hashlib, json, math

ROOT = Path(__file__).resolve().parent
FILE = ROOT / "D56_P2_A_SPATIAL_CONTRACT.json"
OUT = ROOT / "D56_P2_A_PRE3D_AUDIT.json"

def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def diff(a, b):
    return [x - y for x, y in zip(a, b)]

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def interval_overlap(a, b):
    return min(a[1], b[1]) - max(a[0], b[0])

def reachable(edges, start):
    seen = {start}
    pending = [start]
    while pending:
        v = pending.pop()
        for a, b in edges:
            if a == v and b not in seen:
                seen.add(b)
                pending.append(b)
    return seen

def validate(data):
    require(data["source_class"] == "AUTHOR_PRE3D_SPATIAL_RESERVATIONS_NOT_MESH",
            "never claim this JSON is a mesh")
    axes = data["void_axes"]
    require(len(axes) == 2 and len(set(a["id"] for a in axes)) == 2, "two distinct axes")
    a, b = axes
    for axis in axes:
        require(len(axis["start"]) == len(axis["end"]) == 3, "axis must be actual XYZ")
        require(all(math.isfinite(float(t)) for t in axis["start"] + axis["end"]), "finite axis")
        require(axis["minimum_radius_reservation"] > 0, "positive but unbuilt clearance reservation")
    p = a["start"][:2]
    q = b["start"][:2]
    r = diff(a["end"][:2], p)
    s = diff(b["end"][:2], q)
    denominator = cross(r, s)
    require(abs(denominator) > 1e-6, "parallel/collinear XY axes are not a 2-axis crossing")
    theta = math.degrees(math.acos(max(-1, min(1,
        abs(dot(r, s)) / (math.hypot(*r) * math.hypot(*s))))))
    require(theta >= 30, "weakly crossing axes: no convincing different direction")
    v = diff(q, p)
    t = cross(v, s) / denominator
    u = cross(v, r) / denominator
    require(.1 < t < .9 and .1 < u < .9, "no internal planar crossing")
    z_a = a["start"][2] + t * (a["end"][2] - a["start"][2])
    z_b = b["start"][2] + u * (b["end"][2] - b["start"][2])
    dz = abs(z_a - z_b)
    require(dz < min(a["minimum_radius_reservation"], b["minimum_radius_reservation"]),
            "unconnected in Z even for conservative notional radius")
    box = {r["id"]: r["box"] for r in data["activity_regions"]}
    require(len(box) == len(data["activity_regions"]) >= 5,
            "at least five individually authored activity regions")
    for name, bb in box.items():
        for axis in ("x", "y", "z"):
            bounds = bb[axis]
            require(len(bounds) == 2 and bounds[0] < bounds[1], name + " invalid " + axis)
            require(bounds[0] >= data["bounds"][axis][0] and bounds[1] <= data["bounds"][axis][1],
                    name + " out of study bounds")
    shared = data["shared_thickness_reservations"]
    require({(r["a"], r["b"]) for r in shared} >= {("MAKING","RESEARCH"), ("RESEARCH","LIVING")},
            "missing essential actual-shared-thickness *reservation*")
    overlaps = {}
    for reservation in shared:
        a_name, b_name = reservation["a"], reservation["b"]
        require(a_name in box and b_name in box, "unknown shared participant")
        overlap = {axis: interval_overlap(box[a_name][axis], box[b_name][axis])
                   for axis in ("x","y","z")}
        require(all(v > 0 for v in overlap.values()), "shared envelope reservation does not intersect in XYZ")
        overlaps[reservation["id"]] = overlap
    nodes = set(data["access_nodes"])
    edges = data["access_edges"]
    require(all(a in nodes and b in nodes for a,b in edges), "nonexistent access vertex")
    seen = reachable(edges, "WEST_STREET")
    require({"MAKING","RESEARCH","LIVING","UPPER_COMMONS","MARKET_EDGE"} <= seen,
            "street topology lacks one of the required destinations")
    require(("PRIVATE_LOBBY","LIVING") in [tuple(p) for p in edges], "private lobby is not the living access")
    public_nodes = set(data["privacy"]["public_nodes"])
    require(all(not (a in public_nodes and b == "LIVING") for a,b in edges),
            "public realm directly opens into private residence")
    require(data["privacy"]["door_or_auth_separation"].startswith("UNBUILT"),
            "source cannot assert a finished private door")
    cameras = data["designed_camera_intents"]
    require(len(cameras) == 5 and len({c["name"] for c in cameras}) == 5,
            "five independent future camera intents must be defined")
    require(all(c["camera"] == "NOT PLACED IN TRUE3D" for c in cameras),
            "do not misrepresent camera intents as captured images")
    limits = data["verification_limitations"]
    require(limits["art"] == "HOLD" and limits["Minecraft"] == "FORBIDDEN",
            "art/construction gates cannot be promoted from this source-only test")
    for key, value in limits.items():
        if key not in ("art","Minecraft"):
            require(value == "NOT RUN", key + " cannot be certified by this source")
    return {"xy_crossing_angle_degrees": round(theta, 3),
            "crossing_parameters":[round(t, 4),round(u,4)],
            "crossing_z_difference_reservation_only":round(dz,3),
            "shared_box_overlap_reservations_only": overlaps,
            "topologically_reachable_from_street":sorted(seen)}

def should_reject(broken, label):
    try:
        validate(broken)
    except (AssertionError, KeyError, ZeroDivisionError, ValueError) as e:
        return {"name":label, "detected":True, "reason":str(e)}
    raise AssertionError("broken model escaped source preflight: " + label)

def main():
    raw = FILE.read_bytes()
    data = json.loads(raw)
    result = validate(data)
    negatives = []
    p = copy.deepcopy(data)
    p["void_axes"][1]["start"] = [-220, -150, 230]
    p["void_axes"][1]["end"] = [220, 114, 70]
    negatives.append(should_reject(p, "parallel void axis"))
    p = copy.deepcopy(data)
    p["access_edges"] = [e for e in p["access_edges"] if e[1] != "CIVIC_GATE"]
    negatives.append(should_reject(p, "street entrance disconnected"))
    p = copy.deepcopy(data)
    p["shared_thickness_reservations"] = [e for e in p["shared_thickness_reservations"]
                                          if e["id"] != "R_L_SHARED"]
    negatives.append(should_reject(p, "research/living thickness deleted"))
    p = copy.deepcopy(data)
    for room in p["activity_regions"]:
        if room["id"] == "LIVING":
            room["box"]["x"] = [200,240]
    negatives.append(should_reject(p, "living and research envelope no longer overlap"))
    p = copy.deepcopy(data)
    p["access_edges"].append(["CIVIC_GATE","LIVING"])
    negatives.append(should_reject(p, "private living exposed to public"))
    p = copy.deepcopy(data)
    p["verification_limitations"]["saved_glb_and_5_perspective_views"] = "PASS"
    negatives.append(should_reject(p, "false 3D success declaration"))
    report = {"gate":"D56-P2-A AUTHOR SOURCE PREFLIGHT ONLY",
              "source_sha256":hashlib.sha256(raw).hexdigest(),
              **result, "deliberate_negative_controls": negatives,
              "body_clearance":"NOT RUN","real_closed_living_room":"NOT RUN",
              "real_3d_material_subtraction":"NOT RUN","5_saved_model_cameras":"NOT RUN",
              "art":"HOLD","formal_qa":"NOT RUN", "minecraft":"FORBIDDEN",
              "disclaimer":"Intersection of reservational axes/boxes is NOT open 3D geometry, light, structure, or navigability."}
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
