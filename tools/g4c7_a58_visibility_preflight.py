#!/usr/bin/env python3
"""A58 G0 screen-space falsification, NOT 3D/visual, S1, G1, or safety certification."""
from __future__ import annotations
import argparse
import copy
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "artifacts/g4c7-a57-civic-weave-g0/spatial_contract.json"
CANDIDATE = ROOT / "artifacts/g4c7-a58-g0-perspective/camera_hypothesis.json"
EPS = 1e-7

def normalize_a57(original: dict) -> dict:
    p = original["public_heart"]
    return {
        "id": "a57_baseline",
        "camera": p["camera"],
        "floor_z": p["floor"]["z"],
        "portal_assumption": "width was unspecified in A57; assumed only for comparison",
        "thresholds": [
            {"role": t["role"], "center": t["center"],
             "opening_width_m": (4.2 if t["role"] == "maker_culture" else 4.0),
             "room_depth_m": t["desired_room_depth_m"]}
            for t in p["program_thresholds"]
        ],
    }

def assess(case: dict, policy: dict) -> dict:
    """Perspective arithmetic along +Y. DOES NOT model occlusion, real apertures or activity."""
    issues = []
    cam = case["camera"]
    x0, y0, z0 = (float(v) for v in cam["position"])
    floor = float(case["floor_z"])
    height = z0 - floor
    if not math.isclose(height, 1.7, abs_tol=EPS):
        issues.append("EYE_HEIGHT_NOT_1_7")
    look = cam["look_direction"]
    if list(look) != [0, 1, 0]:
        issues.append("UNSUPPORTED_CAMERA_DIRECTION")
    fov = float(cam["horizontal_fov_degrees"])
    width = int(policy["image_width_px"])
    if not 10 < fov < 130 or width < 100:
        raise ValueError("invalid projection config")
    focal = width / (2 * math.tan(math.radians(fov / 2)))
    min_near = float(policy["minimum_near_human_px"])
    min_far = float(policy["minimum_far_human_px"])
    min_aperture = float(policy["minimum_portal_width_px"])
    margin = float(policy["edge_margin_degrees"])
    human = float(policy["reference_human_height_m"])
    rows = []
    slots = []
    roles = set()
    for t in case["thresholds"]:
        role = t["role"]
        if role in roles:
            issues.append("DUPLICATE_ROLE:" + role)
        roles.add(role)
        x, y, z = map(float, t["center"])
        dx, depth_y = x-x0, y-y0
        opening = float(t["opening_width_m"])
        room = float(t["room_depth_m"])
        if depth_y <= EPS:
            issues.append("PORTAL_BEHIND_CAMERA:" + role)
            continue
        if opening <= 0 or room <= 0:
            issues.append("INVALID_OPENING_OR_DEPTH:" + role)
            continue
        angle = math.degrees(math.atan2(dx, depth_y))
        extreme = math.degrees(math.atan2(abs(dx)+opening/2, depth_y))
        portal_px = focal*opening/depth_y
        near_px = focal*human/depth_y
        far_px = focal*human/(depth_y+room)
        center_px = width/2 + focal*dx/depth_y
        half_px = portal_px/2
        row = {"role":role,"angle_deg":round(angle,2),
               "farthest_edge_deg":round(extreme,2),
               "projected_portal_width_px":round(portal_px,2),
               "near_human_px":round(near_px,2),
               "far_human_px":round(far_px,2),
               "projected_center_x_px":round(center_px,2),
               "room_depth_m":room,"portal_z_m":z}
        rows.append(row)
        slots.append((center_px-half_px,center_px+half_px,role))
        if extreme > fov/2-margin+EPS:
            issues.append("FRUSTUM_EDGE:"+role)
        if near_px < min_near:
            issues.append("NEAR_HUMAN_TOO_SMALL:"+role)
        if far_px < min_far:
            issues.append("FAR_HUMAN_TOO_SMALL:"+role)
        if portal_px < min_aperture:
            issues.append("PORTAL_TOO_SMALL:"+role)
        if room < float(policy["minimum_room_depth_m"]):
            issues.append("ROOM_DEPTH_SHORT:"+role)
    if roles != {"market","maker_culture","research_learning"}:
        issues.append("THREE_REQUIRED_PROGRAMS_MISSING")
    for left,right in zip(sorted(slots), sorted(slots)[1:]):
        if left[1] >= right[0]-EPS:
            issues.append("OVERLAPPING_PROJECTED_PORTALS:"+left[2]+"/"+right[2])
    return {
        "id": case["id"],
        "geometry_status": "G0_SCREENSPACE_PROXY_ONLY",
        "perspective_heuristic": "PASS" if not issues else "REJECT_SCREENSPACE",
        "issues": issues,
        "focal_length_px": round(focal,2),
        "cameras_and_geometry_verified": False,
        "rooms_opaque_occlusion_and_daylight_verified": False,
        "art_s1_g1_g2_g3": "NOT_RUN",
        "rows": rows
    }

def svg_report(old: dict, new: dict, policy: dict) -> str:
    width=960
    def panel(items, y0, title, tint):
        parts=[f'<text x="45" y="{y0+29}" fill="{tint}" font-family="sans-serif" font-size="24">{title}</text>',
               f'<rect x="42" y="{y0+45}" width="880" height="193" rx="10" fill="#112c42" stroke="#406078"/>',
               f'<rect x="76" y="{y0+94}" width="812" height="93" fill="#0b1c2d" stroke="#57768a"/>',
               f'<line x1="482" y1="{y0+90}" x2="482" y2="{y0+190}" stroke="#a8bdd0" stroke-dasharray="5,7"/>']
        for q in items["rows"]:
            x=76+(q["projected_center_x_px"]/960)*812
            w=q["projected_portal_width_px"]/960*812
            bad=q["near_human_px"] < policy["minimum_near_human_px"] or q["far_human_px"] < policy["minimum_far_human_px"]
            color="#ed9b8c" if bad else "#8ce8cd"
            parts.extend([f'<rect x="{x-w/2:.1f}" y="{y0+110}" width="{w:.1f}" height="57" fill="{color}" opacity=".85"/>',
            f'<text x="{x:.1f}" y="{y0+212}" fill="#e5f5ee" text-anchor="middle" font-size="13" font-family="sans-serif">{q["role"][:10]}</text>',
            f'<text x="{x:.1f}" y="{y0+126}" fill="#102334" text-anchor="middle" font-size="12" font-family="sans-serif">{q["near_human_px"]:.0f}px</text>'])
        parts.append(f'<text x="52" y="{y0+264}" fill="#b4d2da" font-family="sans-serif" font-size="13">Proxy {items["perspective_heuristic"]}: {"; ".join(items["issues"][:4]) or "No basic screen-space warning"}</text>')
        return '\n'.join(parts)
    a=panel(old,110,"A57 previous contract • projected image-space",'#ffcebb')
    b=panel(new,430,"A58 revised study • projected image-space",'#aaf0df')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 790">
<rect width="960" height="790" fill="#071b30"/>
<text x="45" y="48" fill="#effaf4" font-family="sans-serif" font-size="27" font-weight="bold">A58 • G0 public-heart perspective preflight</text>
<text x="45" y="77" fill="#a7c7cc" font-family="sans-serif" font-size="16">960px / 78° horizontal FOV • 1.7m eye • 1.7m reference human</text>
{a}
{b}
<text x="45" y="752" fill="#ffe2ac" font-family="sans-serif" font-size="14">THIS IS NOT a render, room visibility test, true opening, architectural beauty or G2/G3 safety proof.</text>
</svg>'''

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--output-dir")
    a=parser.parse_args()
    if not a.self_test and not a.evaluate:
        parser.error("choose --self-test and/or --evaluate")
    legacy=json.loads(LEGACY.read_text(encoding="utf-8"))
    data=json.loads(CANDIDATE.read_text(encoding="utf-8"))
    assert data["status"] == "G0_SCREENSPACE_HYPOTHESIS_ONLY"
    assert data["safety"]["minecraft_construction"] == "FORBIDDEN"
    old=assess(normalize_a57(legacy),data["policy"])
    new=assess(data["study"],data["policy"])
    if a.self_test:
        assert old["perspective_heuristic"] == "REJECT_SCREENSPACE", old
        assert new["perspective_heuristic"] == "PASS", new
        for label,mutate in (
            ("camera_too_far",lambda x:x["camera"]["position"].__setitem__(1,-80)),
            ("wrong_eye_height",lambda x:x["camera"]["position"].__setitem__(2,4.1)),
            ("out_of_frustum",lambda x:x["thresholds"][0]["center"].__setitem__(0,-30)),
            ("too_narrow_aperture",lambda x:x["thresholds"][0].__setitem__("opening_width_m",.2)),
            ("depth_missing",lambda x:x["thresholds"][0].__setitem__("room_depth_m",4)),
            ("identical_program",lambda x:x["thresholds"][1].__setitem__("role","market")),
        ):
            altered=copy.deepcopy(data["study"])
            mutate(altered)
            assert assess(altered,data["policy"])["perspective_heuristic"] != "PASS",label
        print("A58_SCREENSPACE_NEGATIVE_CONTROLS_PASS 6/6; art/S1/G1/G2/G3 NOT RUN")
    if a.evaluate:
        report={"stage":"A58","baseline":old,"revised_hypothesis":new,
                "notice":"Pixel arithmetic only; arbitrary review-warning thresholds. No real rooms, material, illumination, line-of-sight, people or construction verified.",
                "all_art_status":"ART_HOLD","s1":"NOT_RUN","g1":"NOT_RUN",
                "g2":"NOT_RUN","g3":"NOT_RUN","minecraft_construction":"FORBIDDEN"}
        print(json.dumps(report,indent=2))
        if a.output_dir:
            target=Path(a.output_dir)
            target.mkdir(parents=True,exist_ok=False)
            (target/"a58_camera_screen_space.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
            (target/"a58_projection_review.svg").write_text(svg_report(old,new,data["policy"])+"\n",encoding="utf-8")
if __name__ == "__main__":
    run()
