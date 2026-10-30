"""D56-P2-D3S12: source-only author-intent guard. No art or GLB certification."""
import copy,json,math
from pathlib import Path
p=Path(__file__).resolve().parent
D=json.loads((p/"D3S12_A_SPATIAL_RESERVATION_SUMMARY.json").read_text(encoding="utf-8"))
def inside(pt,rect):
    return all(rect[0][i]<=pt[i]<=rect[1][i] for i in (0,1))
def check(d):
    m=d["manufacturing"];r=d["research"];l=d["living"];ax=d["axes"];st=d["source_status"]
    assert d["type"]=="AUTHOR INTENT ONLY, NOT BUILT OR REAL GLB"
    assert m["intended_roof_level"]==r["source_level_z"]==160,"shared M roof/R support height"
    assert r["actual_triangle_support"]=="NOT BUILT" and l["actual_roof_floor_door"]=="NOT BUILT","fake building"
    assert inside(r["eye_xyz"],r["intended_shared_M_roof_R_floor_patch_xy"]),"research has no planned platform"
    eye=r["eye_xyz"];target=m["event_target"]
    t=(160-eye[2])/(target[2]-eye[2]);cross=[eye[i]+t*(target[i]-eye[i]) for i in range(3)]
    assert 0<t<1 and inside(cross,m["aperture_xy"]),"research line intersects intended opaque roof"
    assert not inside(eye,m["aperture_xy"]),"research unsupported above opening"
    assert l["private_floor_z"]==l["garden_z"]==240,"private/garden z gap"
    assert inside(l["eye_xyz"],l["private_room_xy"]),"living eye outside private area"
    assert inside(l["garden_target_xyz"],l["garden_xy"]),"target outside garden"
    assert inside(l["garden_target_xyz"],l["shared_R_roof_L_garden_patch_xy"]),"shared R/L garden mismatched"
    door=l["intended_door"]
    assert door["x"]==l["private_room_xy"][0][0]==l["garden_xy"][1][0],"no private threshold"
    assert door["y_min"]<=l["eye_xyz"][1]<=door["y_max"],"door not aligned with living"
    assert ax["actual_civic_rooms"]=="NOT BUILT" and ax["vertical_transfer"]=="NOT BUILT","fake indoor civic rooms"
    a=ax["A"]["start_xyz"];b=ax["A"]["end_xyz"];c=ax["B"]["start_xyz"];e=ax["B"]["end_xyz"]
    u=[b[i]-a[i] for i in range(2)];v=[e[i]-c[i] for i in range(2)]
    det=u[0]*v[1]-u[1]*v[0];assert abs(det)>1e-6,"parallel"
    q=[c[i]-a[i] for i in range(2)]
    t=(q[0]*v[1]-q[1]*v[0])/det;w=(q[0]*u[1]-q[1]*u[0])/det
    assert 0<t<1 and 0<w<1,"axes don't intersect in plan"
    assert abs((a[2]+t*(b[2]-a[2]))-(c[2]+w*(e[2]-c[2])))>5,"no planned height difference"
    assert st["true_glb"]=="NOT BUILT" and st["formal_art_adoptions"]==0,"fake GLB or art"
    assert st["formal_331_993"]=="NOT RUN" and st["formal_G0_S1_G1_G2_G3"]=="NOT RUN","fake formal QA"
    assert not st["minecraft_ed_world_write"] and st["main_unchanged"] and st["PR53_draft"],"protected repo/world"
    return {"research_roof_source_intersection_xyz":[round(x,3) for x in cross],"source_only":True}
positive=check(D)
mutations={
"close research aperture":lambda x:x["manufacturing"].update(aperture_xy=[[-30,-15],[55,75]]),
"move eye off support":lambda x:x["research"].update(eye_xyz=[-35,65,176]),
"mismatch private/garden level":lambda x:x["living"].update(private_floor_z=255),
"break private doorway":lambda x:x["living"]["intended_door"].update(y_min=65),
"parallelize two axes":lambda x:x["axes"]["B"].update(end_xyz=[280,340,170]),
"fake actual shared support":lambda x:x["research"].update(actual_triangle_support="PASS"),
"fake true GLB":lambda x:x["source_status"].update(true_glb="PASS"),
"fake formal QA":lambda x:x["source_status"].update(formal_331_993="PASS"),
"fake ART adoption":lambda x:x["source_status"].update(formal_art_adoptions=1)}
results=[]
for name,fn in mutations.items():
    corrupted=copy.deepcopy(D);fn(corrupted)
    try:check(corrupted);detected=False
    except AssertionError:detected=True
    results.append({"mutation":name,"detected":detected})
assert len(results)==9 and all(x["detected"] for x in results),"source gate failed"
print(json.dumps({"classification":"AUTHOR INTENT ONLY / NOT ART PASS OR ACTUAL GLB",**positive,"tests":results,"detected":9,"total":9},indent=2))
