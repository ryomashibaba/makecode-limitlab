"""D55 independent finite shared-section interference test, PRE-3D only.
Does not import author geometry source. Discrete point probes, NOT a swept-body
safety claim. Detects A1 blocked path and tests A2 abstract edge notches.
"""
import json,copy,math
from pathlib import Path
R=Path(__file__).resolve().parent
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def add(a,b):return [x+y for x,y in zip(a,b)]
def sub(a,b):return [x-y for x,y in zip(a,b)]
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def scale(a,k):return [k*x for x in a]
def norm(a):return math.sqrt(dot(a,a))
def patch_geom(s):
    owners=s["owners"]
    mean=[sum(s["owner_deltas"][o][i] for o in owners)/len(owners) for i in range(3)]
    p=add(s["base_origin"],mean)
    u=add(s["u"],[mean[1]*.35,-mean[0]*.28,mean[2]*.24])
    v=add(s["v"],[-mean[0]*.23,mean[2]*.19,mean[1]*.31])
    n=cross(u,v);n=scale(n,1/norm(n))
    return p,u,v,n,s["thickness"]*(1+.07*len(owners))
def inside_material(point,section):
    o,u,v,n,thick=patch_geom(section)
    d=sub(point,o)
    perpendicular=dot(d,n)
    if abs(perpendicular)>thick/2:return False
    uu=dot(u,u);uv=dot(u,v);vv=dot(v,v)
    det=uu*vv-uv*uv
    assert det>1
    coord_u=(dot(d,u)*vv-dot(d,v)*uv)/det
    coord_v=(dot(d,v)*uu-dot(d,u)*uv)/det
    if max(abs(coord_u),abs(coord_v))>1:return False
    for hole in section.get("route_apertures",[]):
        if hole["local_u"][0]<=coord_u<=hole["local_u"][1] and hole["local_v"][0]<=coord_v<=hole["local_v"][1]:
            return False
    return True
def scan(d):
    programs=d["programs"];w=d["walk"]
    counts={s["id"]:0 for s in d["shared_thick_sections"]}
    first={}
    samples=0
    for leg in w["legs"]:
        p=programs[leg["from"]]["foot"];q=programs[leg["to"]]["foot"]
        dx=q[0]-p[0];dy=q[1]-p[1];length=math.hypot(dx,dy)
        flat=(length-leg["steps"]*w["run"])/2
        sidevec=[-dy/length,dx/length]
        for i in range(251):
            t=i/250
            progress=max(0,min(1,(t*length-flat)/(leg["steps"]*w["run"])))
            height=p[2]+progress*leg["steps"]*w["rise"]
            for side in (-w["sample_width"]/2,0,w["sample_width"]/2):
                for h in (.15,1.65,w["sample_headroom"]):
                    point=[p[0]+t*dx+side*sidevec[0],p[1]+t*dy+side*sidevec[1],height+h]
                    samples+=1
                    for sec in d["shared_thick_sections"]:
                        if inside_material(point,sec):
                            counts[sec["id"]]+=1
                            if sec["id"] not in first:
                                first[sec["id"]]={"leg":leg["from"]+"->"+leg["to"],"fraction":round(t,4),
                                                  "point":point}
    return {"probes":samples,"hits_per_section":counts,"total_hits":sum(counts.values()),"first_hit":first}
def main():
    a1=json.loads((R/"D55_A_SHARED_SECTION_CONTRACT.json").read_text())
    a2=json.loads((R/"D55_A2_APERTURE_CONTRACT.json").read_text())
    original=scan(a1)
    assert original["total_hits"]>0 and original["hits_per_section"]["maker_research_transition"]>0
    assert original["hits_per_section"]["research_living_privacy_section"]>0
    revised=scan(a2)
    assert revised["total_hits"]==0,("A2 proposed openings still have sampled intersections",revised)
    broken=copy.deepcopy(a2)
    for s in broken["shared_thick_sections"]:s.pop("route_apertures",None)
    assert scan(broken)["total_hits"]==original["total_hits"],"removed notches should restore obstruction"
    evidence={"A1":"PRE-3D REJECT - uncut shared thick material intersects route probes",
       "A1_probe_audit":original,"A2":"DISCRETE PROBE CLEAR ONLY - not walkable GLB",
       "A2_probe_audit":revised,"negative_control_cutouts_removed":True,
       "real_mesh_cutouts":"NOT RUN","continuous_body_sweep":"NOT RUN",
       "real_sunlight":"NOT RUN","visual_art":"HOLD/NOT JUDGED",
       "formal_331_993":"NOT RUN","formal_G0_S1_G1_G2_G3":"NOT RUN",
       "Minecraft":"FORBIDDEN"}
    (R/"D55_A1_A2_INTERFERENCE_AUDIT.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(evidence,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
