#!/usr/bin/env python3
"""M37-P2 ART-FIRST capability gate: do not "fix" an absent city with box edits.

This examines *genuine native Blender provenance evidence*, not a sketch,
model hallucination, or an unrelated rendered image. It authorizes NO ART PASS
or Minecraft construction. A known missing city, inhabitable rooms, shipyard
and public boundary must be directly authored in a new artist-led source
before we run more blind extrude/inset repairs.

Usage:
  python tools/g4c7_m37p2_art_gap_authoring_gate.py \
    --native-report P2_NATIVE_PAIRED_THREE_VIEW_REPORT.json \
    --feedback P2_REAL_IMAGE_ART_FEEDBACK.json --out ART_GAP_DECISION.json
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

VIEWS=("AERIAL","PUBLIC_EYE","HABITAT_EYE")
REQUIRED_ROLES={
    "city_macro": "P2_CITY_MACRO_DIRECT_AUTHOR",
    "inhabited_section": "P2_INHABITED_SECTION_DIRECT_AUTHOR",
    "public_factory_boundary": "P2_PUBLIC_FACTORY_BOUNDARY_DIRECT_AUTHOR",
    "research_culture": "P2_RESEARCH_CULTURE_DIRECT_AUTHOR",
    "habitat_private": "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
}
UNAUTHORED_FLAGS=("factory_boundary","research_culture","habitat_living_interior")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def decide(native,feedback):
    """Read two reports that already have SHA-bound native Cycles images."""
    errors=[]
    if not isinstance(native,dict) or not isinstance(feedback,dict):
        raise ValueError("EVIDENCE_OBJECTS_REQUIRED")
    if native.get("art")!="HOLD" or feedback.get("art")!="HOLD":
        errors.append("ART_HOLD_MUST_REMAIN")
    if native.get("official_adoptions")!=0 or feedback.get("official_adoptions")!=0:
        errors.append("FORMAL_ADOPTION_MUST_BE_ZERO")
    if native.get("minecraft")!="FORBIDDEN" or feedback.get("minecraft")!="FORBIDDEN":
        errors.append("MINECRAFT_WORLD_WRITE_FORBIDDEN")
    if native.get("formal_331_993")!="NOT_RUN" or feedback.get("formal_331_993")!="NOT_RUN":
        errors.append("FORMAL_SAFETY_NOT_RUN_REQUIRED")
    if feedback.get("original_stored_blend_sha256")!=native.get("original_stored_blend_sha256"):
        errors.append("FEEDBACK_NOT_LINKED_TO_NATIVE_BLEND")
    if not isinstance(native.get("original_stored_blend_sha256"),str) or len(native["original_stored_blend_sha256"])!=64:
        errors.append("MISSING_REAL_NATIVE_BLEND_SHA")
    views=native.get("views",{})
    if not isinstance(views,dict) or set(views)!=set(VIEWS):
        errors.append("THREE_NATIVE_CYCLES_VIEWS_REQUIRED")
    if not isinstance(feedback.get("verified_images_sha256"),dict) or set(feedback.get("verified_images_sha256",{}))!=set(VIEWS):
        errors.append("FEEDBACK_MUST_BIND_ALL_THREE_IMAGES")
    else:
        for key in VIEWS:
            if native.get("views",{}).get(key,{}).get("sha256") != feedback["verified_images_sha256"][key]:
                errors.append("IMAGE_DIGEST_MISMATCH_"+key)
    if feedback.get("outcome") not in ("EARLY_ART_REJECT","ART_HOLD_VISUAL_JUDGMENT_REQUIRED"):
        errors.append("INVALID_FEEDBACK_OUTCOME")
    if errors:
        return {
            "schema":"g4c7-m37p2-authoring-capability-gate-v1",
            "decision":"EVIDENCE_INVALID_SAFE_STOP",
            "reason_codes":sorted(set(errors)),
            "permitted_model_calls":0,"automatic_geometry_repair_allowed":False,
            "art":"HOLD","official_adoptions":0,"minecraft":"FORBIDDEN",
        }

    deficiencies=[]
    if native.get("true_city") is False:
        deficiencies.append("WHOLE_DENSE_CITY_NOT_AUTHORED")
    for field in UNAUTHORED_FLAGS:
        if native.get(field)=="NOT_AUTHORED":
            deficiencies.append("UNAUTHORED_"+field.upper())
    roles=native.get("roles",{})
    if isinstance(roles,dict) and set(roles)=={"city_macro","habitat"} and all(
        isinstance(role,dict) and role.get("vertices")==8 and role.get("faces")==6
        for role in roles.values()
    ):
        deficiencies.append("ONLY_TWO_TECHNICAL_CUBOIDS")
    reasons=feedback.get("reasons",[])
    if not isinstance(reasons,list):
        deficiencies.append("VISUAL_REASON_LIST_MALFORMED")
    elif "TWO_CUBOIDS_8_VERTICES_6_FACES_EACH" in reasons:
        deficiencies.append("VISUALLY_CONFIRMED_TWO_CUBOIDS")
    if feedback["outcome"]=="EARLY_ART_REJECT":
        deficiencies.append("EARLY_ART_REJECT_FROM_ACTUAL_CYCLES_IMAGES")

    # The existence of surfaces/rooms cannot be proven from a role name,
    # face count, or AI commentary. A human must inspect actual 3D and views.
    unsolved=bool(deficiencies)
    return {
        "schema":"g4c7-m37p2-authoring-capability-gate-v1",
        "decision":"REQUIRE_NEW_DIRECT_AUTHOR_3D_CONTENT" if unsolved
                   else "ART_HOLD_HUMAN_VISUAL_REVIEW_REQUIRED",
        "reason_codes":sorted(set(deficiencies)),
        "source_blend_sha256":native["original_stored_blend_sha256"],
        "visual_sha256_by_view":feedback["verified_images_sha256"],
        "minimum_author_deliverables": [
            "One continuous city macro with visible urban density and varied inhabited fronts",
            "A real street-to-entrance-to-vestibule-to-living-room-to-window section",
            "Actual spacecraft assembly/rigging/inspection equipment and separate staff floors",
            "Physically thick public visitor gallery/window/barrier, not a painted color stripe",
            "Research and cultural rooms with actual objects, daylight and real vertical circulation",
            "All five named collections populated by direct authored, distinct native meshes",
            "Same saved authored .blend, aerial/public-eye/habitat-eye genuinely rendered"
        ],
        "reused_rejected_box_city_forbidden":True,
        "repaired_two_box_as_formal_art_forbidden":True,
        "automatic_geometry_repair_allowed":False if unsolved else False,
        "permitted_model_calls":0,
        "review_cameras_artist_approved":False,
        "human_art_approval_required":True,
        "art":"HOLD","official_adoptions":0,
        "formal_331_993":"NOT_RUN","minecraft":"FORBIDDEN",
        "makecode":"NOT_EVALUATED",
        "work":"NOT_USED",
    }

def run(native_report, feedback_report, output):
    src=Path(native_report).resolve()
    fp=Path(feedback_report).resolve()
    out=Path(output).resolve()
    if out.exists():
        raise FileExistsError("APPEND_ONLY_GATE_DECISION_EXISTS")
    native=json.loads(src.read_text(encoding="utf-8"))
    feedback=json.loads(fp.read_text(encoding="utf-8"))
    result=decide(native,feedback)
    result["native_report_sha256"]=sha(src)
    result["feedback_report_sha256"]=sha(fp)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("P2_ARTIST_SOURCE_GAP_GATE",result["decision"],
          "model_calls=0","official_adoptions=0",flush=True)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--native-report",required=True)
    p.add_argument("--feedback",required=True)
    p.add_argument("--out",required=True)
    args=p.parse_args()
    result=run(args.native_report,args.feedback,args.out)
    return 2 if result["decision"]=="EVIDENCE_INVALID_SAFE_STOP" else 0

if __name__=="__main__":
    sys.exit(main())
