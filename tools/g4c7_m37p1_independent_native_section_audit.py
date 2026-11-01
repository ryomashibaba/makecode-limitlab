#!/usr/bin/env python3
"""M37-P1 independent native reopen, real geometry cross-program checks, and
in-memory negative controls. No safety/ART pass; no world writes.
"""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector

ROOT=Path("artifacts/g4c7-m37p1-shared-section-build")
SOURCE=Path("artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/M37O_A_REAL_ACTIVITY_SILHOUETTE_AUTHOR_ART_HOLD.blend")
SOURCE_PIN="7845343514b79067835ddbbd18aabf93439a391f4a2c0983227475b18331b2f1"
SPEC=Path("research/g4c7-b11-r5-d56/p2/d3s26/M37P0_SHARED_AUTHOR_DECISION_SOURCE_OF_FORM_V1.json")
man=json.loads((ROOT/"M37P1_AUTHOR_MANIFEST.json").read_text())
native=ROOT/man["native_blend"]["name"]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(SOURCE)==SOURCE_PIN and sha(SPEC)==man["source_contract_sha256"]
assert native.read_bytes().startswith(b"BLENDER")
assert sha(native)==man["native_blend"]["sha256"]
assert man["art"]=="EARLY_REVIEW_REQUIRED_UNAPPROVED"
assert man["formal_adoption"]==0 and man["Minecraft"]=="FORBIDDEN"
assert man["formal_331_993"]==man["S1_G1_G2_G3"]=="NOT_RUN"
assert man["old_pavilions_and_tubes_imported"]==0
bpy.ops.wm.open_mainfile(filepath=str(native.resolve()))
sc=bpy.data.scenes[man["native_scene"]]
assert sc["M37P1_ART"]=="EARLY_REVIEW_UNJUDGED"
assert sc["M37P1_ART_ADOPTION"]==0 and sc["M37P1_MINECRAFT"]=="FORBIDDEN"
assert sc["M37P1_331_993"]==sc["M37P1_G0_S1_G1_G2_G3"]=="NOT_RUN"
assert sc["M37P1_PREVIOUS_ART"]=="M37O1_EARLY_REJECT"
m={o.name:o for o in sc.objects if o.type=="MESH"}
c={o.name:o for o in sc.objects if o.type=="CAMERA"}
assert len(c)==9 and len(man["cameras"])==9
assert len(man["same_saved_native_renders"])==7
assert not any(n.startswith(("M37L_","M37M_","M37N_","M37O_")) for n in m)
for entry in man["same_saved_native_renders"].values():
    p=ROOT/entry["name"]
    assert p.read_bytes()[:8]==b"\x89PNG\r\n\x1a\n"
    assert sha(p)==entry["sha256"]
C=man["shared_author_decisions"]["shared_maker_clearance"]
D=man["shared_author_decisions"]["research_daylight_transfer"]
H=man["shared_author_decisions"]["habitat_graded_threshold"]
U=man["shared_author_decisions"]["upper_civic_link"]
assert 48<=C<=60 and 8<=D<=16 and 8<=H<=14 and 14<=U<=21
def near(a,b):
    return abs(float(a)-float(b))<1e-3
def first_z(n):
    return m["M37P1_"+n].data.vertices[0].co.z
def max_z(n):
    return max(v.co.z for v in m["M37P1_"+n].data.vertices)
def validate_native():
    assert all("M37P1_"+x in m for x in (
        "ARRIVAL_FOLDED_GROUND","COMMONS_LARGE_COURT",
        "MAKER_OBSERVATION_LEDGE","RESEARCH_SHARED_PLAZA",
        "HABITAT_PRIVATE_COURT","CULTURE_CIVIC_FORUM",
        "UPPER_OPEN_SKY_DECK","SPACECRAFT_REAL_ASSEMBLY_TEST_ARTIFACT",
        "SHIPYARD_ACTUAL_PUBLIC_STAFF_SEAL",
        "HABITAT_PRIVATE_VIEW_BREAK","GANTRY_OCCUPIED_LOFT"))
    assert near(first_z("MAKER_OBSERVATION_LEDGE"),23+D*.32)
    assert near(first_z("RESEARCH_SHARED_PLAZA"),30+D*.55)
    assert near(first_z("GANTRY_OCCUPIED_LOFT"),C+12)
    assert near(max_z("WEST_TECTONIC_MAKER_WING"),C+14)
    assert near(max_z("SHIPYARD_ACTUAL_PUBLIC_STAFF_SEAL"),35+D*.52)
    assert near(first_z("HABITAT_PRIVATE_COURT"),31+H*.5)
    assert near(max_z("HABITAT_PRIVATE_VIEW_BREAK"),44+H*.9)
    assert near(first_z("CULTURE_CIVIC_FORUM"),44+U*.32)
    assert near(first_z("UPPER_OPEN_SKY_DECK"),57+U*.52)
    barrier=m["M37P1_SHIPYARD_ACTUAL_PUBLIC_STAFF_SEAL"]
    assert barrier["P1_ROLE"]=="SEALED_BARRIER_NOT_FIRE_IMPACT_OR_ACCESS_CERTIFIED"
    private=m["M37P1_HABITAT_PRIVATE_VIEW_BREAK"]
    assert private["P1_ROLE"]=="ACTUAL_PRIVATE_SCREEN_NO_PUBLIC_PASSAGE"
    assert len(m["M37P1_SPACECRAFT_REAL_ASSEMBLY_TEST_ARTIFACT"].data.vertices)==126
    for tag,names in man["actual_native_meshes_tied_to_author_decisions"].items():
        assert len(names)>=5
        assert len(names)==len(set(names))
        for name in names:
            assert name in m
            assert tag in m[name]["P1_DECISIONS"].split("|")
            assert len(m[name].data.vertices)>=4
            assert len(m[name].data.polygons)>=2
        assert any(x["P1_PROGRAMS"].count("|")>=1
                   for x in (m[n] for n in names))
    return True
assert validate_native()
rejections=[]
def expect_reject(name,modify,restore):
    modify()
    try:
        validate_native()
    except (AssertionError,KeyError):
        rejections.append(name)
    else:
        raise AssertionError("NEGATIVE_CONTROL_NOT_DETECTED:"+name)
    finally:
        restore()
def move_vertex(ob,delta):
    ob.data.vertices[0].co.z+=delta
def revert_vertex(ob,delta):
    ob.data.vertices[0].co.z-=delta
for n,label in (
    ("GANTRY_OCCUPIED_LOFT","maker_clearance_uncoupled"),
    ("RESEARCH_SHARED_PLAZA","research_daylight_uncoupled"),
    ("HABITAT_PRIVATE_COURT","habitat_threshold_uncoupled"),
    ("UPPER_OPEN_SKY_DECK","upper_civic_uncoupled")):
    ob=m["M37P1_"+n]
    expect_reject(label,lambda ob=ob:move_vertex(ob,3),
                  lambda ob=ob:revert_vertex(ob,3))
bar=m["M37P1_SHIPYARD_ACTUAL_PUBLIC_STAFF_SEAL"]
oldrole=bar["P1_ROLE"]
expect_reject("factory_public_seal_removed",
              lambda:bar.__setitem__("P1_ROLE","PUBLIC_UNRESTRICTED"),
              lambda:bar.__setitem__("P1_ROLE",oldrole))
p=m["M37P1_HABITAT_PRIVATE_VIEW_BREAK"]
oldrole=p["P1_ROLE"]
expect_reject("private_habitat_threshold_erased",
              lambda:p.__setitem__("P1_ROLE","NO_PRIVACY"),
              lambda:p.__setitem__("P1_ROLE",oldrole))
assert len(rejections)==6 and validate_native()
# Controls are in memory only. Source file and newly saved native original are
# unchanged. This does NOT demonstrate sound construction or free walking.
assert sha(native)==man["native_blend"]["sha256"]
assert sha(SOURCE)==SOURCE_PIN
result={
 "result":"LIMITED_M37P1_NATIVE_SHARED_AUTHOR_METHOD_REOPEN_PASS",
 "parent_source_original_unchanged":True,
 "new_native_saved_sha256":sha(native),
 "shared_intent_mesh_dependency_tags_verified":list(man["shared_author_decisions"]),
 "coupled_real_geometry_coefficient_checks":9,
 "same_native_fixed_cameras":len(c),
 "same_native_render_sha_verified":7,
 "physical_negative_controls_rejected":rejections,
 "new_city_art":"UNREVIEWED_NEVER_AUTOMATIC_PASS",
 "full_city_density":"NOT_CERTIFIED",
 "human_walking_331_993":"NOT_RUN","S1_G1_G2_G3":"NOT_RUN",
 "public_private_worker_separation":"GEOMETRY_ONLY_NOT_CERTIFIED",
 "human_path_sweep":"NOT_RUN",
 "structural_support":"NOT_CERTIFIED",
 "MakeCode_cost":"NOT_RUN",
 "Minecraft":"FORBIDDEN",
 "official_adoption":0
}
(ROOT/"M37P1_INDEPENDENT_NATIVE_AUDIT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2))
print("M37P1_INDEPENDENT_NATIVE_NOT_ART_PASS",json.dumps(result,ensure_ascii=False),flush=True)
