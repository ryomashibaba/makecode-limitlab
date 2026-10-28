"""Independent from d27_scene_author.py: inspect SAVED D27 author source and 2D geometry only."""
import argparse,json,math,copy
from pathlib import Path
from xml.etree import ElementTree as ET

def intersect(a,b,c,d):
    def cross(p,q,r):
        return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    aa,bb=cross(a,b,c),cross(a,b,d)
    cc,dd=cross(c,d,a),cross(c,d,b)
    return (aa*bb< -1e-8 and cc*dd< -1e-8)
def angle(eye,a,b):
    u=(a[0]-eye[0],a[1]-eye[1])
    v=(b[0]-eye[0],b[1]-eye[1])
    return math.degrees(math.acos(max(-1.,min(1.,(u[0]*v[0]+u[1]*v[1])/math.hypot(*u)/math.hypot(*v)))))
def audit_original(doc,cases):
    p=doc["protection"]
    assert p=={"art":"ART HOLD","adopted":0,"formal_G0":"NOT_RUN","formal_S1_G1_G2_G3":"NOT_RUN",
       "true_3d":"NOT_RUN","upper_level_continuous_path":"NOT_MODELED",
       "minecraft_construction":"FORBIDDEN","city_integration":"FORBIDDEN","main":"UNTOUCHED","PR53":"DRAFT_OPEN"}
    assert doc["stage"]=="B11-R5 D27" and doc["study"]=="SCENE_FIRST_AUTHOR_2D_ONLY"
    assert [x["id"] for x in doc["scenes"]]==["arrival","making","exchange","research","upper"]
    assert sorted(x["id"] for x in doc["candidates"])==["A","B"]
    res=[]
    for c in doc["candidates"]:
        eye=c["view_eye"];mk=c["maker_target"];rs=c["research_target"]
        blocked={role:[i for i,(x,y) in enumerate(c["enclosure"]) if intersect(eye,target,x,y)]
             for role,target in (("maker",mk),("research",rs))}
        ground=c["route"]
        assert len(ground)>=8 and len(set(tuple(x) for x in ground))==len(ground)
        assert all(math.dist(a,b)<40 for a,b in zip(ground,ground[1:]))
        # Not a 3D floor or route, merely 2D segment regularity.
        roles={x["id"]:x["role"] for x in c["program"]}
        case=cases[c["id"]]
        assert case["all_roles"]==roles
        assert case["baseline"]==list(roles)
        for deleted,role in (("no_maker","maker"),("no_research","research")):
            expected=[k for k in roles if roles[k]!=role]
            assert case[deleted]==expected
            assert not any(roles[k]==role for k in case[deleted])
        assert len(c["section_profile"])>=8 and len(c["vertical_cores"])==2
        res.append({"id":c["id"],"2d_view_angle_degrees":round(angle(eye,mk,rs),3),
           "2d_other_role_wall_blockers":blocked,
           "author_roles_present":list(roles),
           "counterfactual_dedicated_role_cleanup":"PASS_AS_ROLE_DATA_ONLY",
           "2d_ground_polyline_segments":len(ground)-1,
           "upper_level_continuous_3d_route":"NOT_MODELED",
           "true_3d":"NOT_RUN","art":"NOT_ADOPTED"})
    return res
def audit_svg(p):
    root=ET.parse(p).getroot(); ns="{http://www.w3.org/2000/svg}"
    assert root.tag==ns+"svg"
    assert len(list(root.iter(ns+"polygon")))>=5
    assert "TRUE 3D" in "".join(x.text or "" for x in root.iter(ns+"text")) or "NOT 3D" in "".join(x.text or "" for x in root.iter(ns+"text"))
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",default="d27_build");o=Path(ap.parse_args().out)
    d=json.loads((o/"d27_author_original.json").read_text(encoding="utf-8"))
    c=json.loads((o/"d27_role_counterfactuals.json").read_text(encoding="utf-8"))
    for x in ("a","b"):audit_svg(o/f"d27_{x}_plate.svg")
    result=audit_original(d,c)
    assert all(not r["2d_other_role_wall_blockers"]["maker"] and not r["2d_other_role_wall_blockers"]["research"] for r in result if r["id"]=="A")
    assert any(r["2d_other_role_wall_blockers"]["maker"] or r["2d_other_role_wall_blockers"]["research"] for r in result if r["id"]=="B")
    # Independently falsifiable boundary: no forged artistic adoption or removed-role residue.
    bad=copy.deepcopy(d);bad["protection"]["adopted"]=1
    try:audit_original(bad,c)
    except AssertionError:pass
    else:raise AssertionError("forged adoption accepted")
    bad=copy.deepcopy(c);bad["A"]["no_maker"].append("maker_workshop")
    try:audit_original(d,bad)
    except AssertionError:pass
    else:raise AssertionError("activity-specific residue undetected")
    bad=copy.deepcopy(d);bad["scenes"].pop()
    try:audit_original(bad,c)
    except AssertionError:pass
    else:raise AssertionError("missing scene undetected")
    bad=copy.deepcopy(d);bad["protection"]["true_3d"]="PASS"
    try:audit_original(bad,c)
    except AssertionError:pass
    else:raise AssertionError("invented 3D validation accepted")
    out={"stage":"D27","scope":"2D_SAVED_AUTHOR_GEOMETRY_ONLY","candidates":result,
        "negative_controls":4,"formal_3D_and_safety":"NOT_RUN",
        "automatic_beauty_judgment":"FORBIDDEN",
        "author_image_review":"REQUIRED_SEPARATELY","art":"ART HOLD",
        "adopted":0,"minecraft":"FORBIDDEN"}
    (o/"d27_independent_2d_result.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("D27 independent 2D source check + 4 mutations PASS. NOT an art/3D/safety result.")
if __name__=="__main__":main()
