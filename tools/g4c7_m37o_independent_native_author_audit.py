#!/usr/bin/env python3
"""Independent native Blender reopen and deliberately failing negatives.
Only a source/authoring proof; ART HOLD and all formal Minecraft safety NOT RUN.
"""
import bpy,hashlib,json,math
from pathlib import Path
ROOT=Path("artifacts/g4c7-m37o-activity-section-build")
PARENT=Path("artifacts/g4c7-m37n-verified-native-maker-exposure-art-hold/M37N_MAKER_SHELL_DIRECT_EDIT_ART_HOLD.blend")
PIN="0817bf8a9681e9380b8167e75ddc236dbcab18920b01298c5e405ed46752bdff"
man=json.loads((ROOT/"M37O_AUTHOR_MANIFEST.json").read_text())
native=ROOT/man["native_blend"]["file"]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(PARENT)==PIN
assert sha(native)==man["native_blend"]["sha256"]
assert native.read_bytes().startswith(b"BLENDER")
assert man["official_adoption"]==0 and man["Minecraft"]=="FORBIDDEN"
assert man["formal_331_993"]=="NOT_RUN" and man["S1_G1_G2_G3"]=="NOT_RUN"
assert man["old_tube_meshes_imported"]==0
assert man["art"]=="EARLY_REVIEW_REQUIRED"
bpy.ops.wm.open_mainfile(filepath=str(native.resolve()))
sc=bpy.data.scenes[man["scene"]]
assert sc["M37O_ART"]=="EARLY_REVIEW_REQUIRED_NOT_PASSED"
assert sc["M37O_MINECRAFT"]=="FORBIDDEN"
assert sc["M37O_FORMAL_331_993"]=="NOT_RUN"
assert sc["M37O_USER_ADOPTION"]==0
mesh={ob.name:ob for ob in sc.objects if ob.type=="MESH"}
cams={ob.name:ob for ob in sc.objects if ob.type=="CAMERA"}
assert len(cams)==9 and len(man["cameras"])==9
assert not any(x.startswith(("M37L_","M37M_","M37N_")) for x in mesh)
assert len(man["programs"])==7
assert len([n for n in mesh if n.startswith("M37O_ROUTE_")])==6
assert len(man["physical_public_route_stations"])==7
def validate():
    assert "M37O_MAKER_PUBLIC_SECURITY_PARTITION" in mesh
    assert mesh["M37O_MAKER_PUBLIC_SECURITY_PARTITION"]["M37O_ROLE"]=="ACTUAL_IMPASSABLE_STAFF_PUBLIC_BARRIER"
    assert "M37O_SHIPYARD_REAL_VEHICLE_MASS" in mesh
    assert len(mesh["M37O_SHIPYARD_REAL_VEHICLE_MASS"].data.vertices)==96
    assert "M37O_PUBLIC_FABRICATION_VIEW_BAY" in mesh
    assert len([n for n in mesh if n.startswith("M37O_ROUTE_")])==6
    assert not any(n.startswith(("M37L_","M37N_","M37M_")) for n in mesh)
    for p in man["programs"]:
        ident=p["id"];poly=p["outline"];z=p["z"]
        f=mesh["M37O_"+ident+"_OCCUPIED_FLOOR"]
        roof=mesh["M37O_"+ident+"_ROOF_SILHOUETTE"]
        assert f["M37O_ROLE"]=="REAL_PROGRAM_FLOOR"
        assert roof["M37O_ROLE"]=="PROGRAM_DETERMINES_CITY_SILHOUETTE"
        assert len(f.data.vertices)==len(roof.data.vertices)==2*len(poly)
        actual=[(v.co.x,v.co.y) for v in f.data.vertices[:len(poly)]]
        assert all(math.dist(a,b)<1e-4 for a,b in zip(actual,poly))
        for a,b in zip(f.data.vertices[:len(poly)],roof.data.vertices[:len(poly)]):
            assert math.dist((a.co.x,a.co.y),(b.co.x,b.co.y))<1e-4
        assert "M37O_"+ident+"_WALL_"+str(p["door"]) not in mesh
        assert "M37O_"+ident+"_DOOR_LEFT" in mesh
        assert "M37O_"+ident+"_DOOR_RIGHT" in mesh
        assert "M37O_"+ident+"_DOOR_HEADER" in mesh
        head=mesh["M37O_"+ident+"_DOOR_HEADER"]
        assert min(v.co.z for v in head.data.vertices)>z+3.99
    return True
assert validate()
assert len(man["same_native_blend_renders"])==5
for item in man["same_native_blend_renders"].values():
    png=ROOT/item["file"]
    assert png.read_bytes()[:8]==b"\x89PNG\r\n\x1a\n"
    assert sha(png)==item["sha256"]
# Deliberately violate the real reopened native scene. All three errors MUST
# be rejected, and mutations are never written back to the original.
neg=[]
def reject(tag,fn,restore):
    fn()
    try:
        validate()
    except (AssertionError,KeyError):
        neg.append(tag)
    else:raise AssertionError("NEGATIVE_CONTROL_UNDETECTED:"+tag)
    finally:restore()
bar=mesh["M37O_MAKER_PUBLIC_SECURITY_PARTITION"]
old_role=bar["M37O_ROLE"]
reject("staff_boundary_removed",
       lambda:bar.__setitem__("M37O_ROLE","NONE"),
       lambda:bar.__setitem__("M37O_ROLE",old_role))
door="M37O_HABITAT_WALL_3"
ref=mesh["M37O_HABITAT_DOOR_HEADER"]
mesh[door]=ref
reject("habitat_entry_sealed",lambda:None,lambda:mesh.pop(door))
rname=next(n for n in mesh if n.startswith("M37O_ROUTE_"))
ro=mesh.pop(rname)
reject("public_link_missing",lambda:None,lambda:mesh.__setitem__(rname,ro))
assert validate() and len(neg)==3
assert sha(PARENT)==PIN and sha(native)==man["native_blend"]["sha256"]
audit={
 "result":"LIMITED_M37O1_SAVED_NATIVE_AUTHOR_METHOD_CONFIRMED",
 "new_city_art":"EARLY_REVIEW_REQUIRED_NOT_PASSED",
 "old_art_reused":False,
 "source_parent_sha256":PIN,
 "source_parent_unchanged":True,
 "authored_programs":len(man["programs"]),
 "nine_scene_cameras":len(cams),
 "five_real_native_render_files_hash_verified":5,
 "genuine_floor_roof_and_open_wall_seam":True,
 "physical_negative_controls_rejected":neg,
 "full_urban_density":"UNREVIEWED",
 "walkable_331_993":"NOT_RUN",
 "S1_G1_G2_G3":"NOT_RUN",
 "human_continuous_sweep":"NOT_CERTIFIED",
 "maker_public_access_protection":"NOT_CERTIFIED",
 "private_habitat_security":"NOT_CERTIFIED",
 "structure_and_egress":"NOT_CERTIFIED",
 "MakeCode_cost":"NOT_EVALUATED",
 "Minecraft":"FORBIDDEN","official_adoption":0,
 "native_sha256":sha(native)
}
(ROOT/"M37O_INDEPENDENT_NATIVE_AUDIT.json").write_text(json.dumps(audit,indent=2,ensure_ascii=False))
print("M37O_INDEPENDENT_METHOD_ONLY",json.dumps(audit,ensure_ascii=False),flush=True)
