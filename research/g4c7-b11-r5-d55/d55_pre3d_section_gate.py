"""D55 PRE-3D numerical veto gate; ONLY author-authored geometry constraints.

Do NOT mistake a passing abstract envelope and multi-owner face test for actual
watertight 3D, supported inhabitable space, daylight or architectural beauty.
Python standard library only; does not import earlier failed model code.
"""
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CONTRACT=ROOT/"D55_A_SHARED_SECTION_CONTRACT.json"

def sub(a,b):
    return [x-y for x,y in zip(a,b)]

def add(a,b):
    return [x+y for x,y in zip(a,b)]

def mul(a,s):
    return [x*s for x in a]

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def norm(a):
    return math.sqrt(dot(a,a))

def cross(a,b):
    return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]

def envelope_value(point,env):
    return sum(((point[k]-env["center"][k])/env["radii"][k])**2 for k in range(3))

def section_patch(item,active):
    # This is a proposed 3D material *boundary*; not a filled closed GLB.
    owners=[o for o in item["owners"] if o in active]
    if not owners:
        return None
    avg=[sum(item["owner_deltas"][o][i] for o in owners)/len(owners) for i in range(3)]
    origin=add(item["base_origin"],avg)
    # Distinct program occupancy demand deforms the same shared surface,
    # rather than only deleting a program-specific slab.
    u=add(item["u"],[avg[1]*.35,-avg[0]*.28,avg[2]*.24])
    v=add(item["v"],[-avg[0]*.23,avg[2]*.19,avg[1]*.31])
    normal=cross(u,v)
    assert norm(normal)>5,(item["id"],"degenerate shared surface")
    assert abs(normal[0])+abs(normal[1])>.1, (item["id"],"flat horizontal shelf")
    thick=item["thickness"]*(1.0+.07*len(owners))
    corners=[add(origin,add(mul(u,a),mul(v,b))) for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]]
    return {"id":item["id"],"owners_present":owners,"corners":corners,
            "thickness":thick,"normal":normal,"opening":item["opening"]}

def sample_walk(contract):
    p=contract["programs"]
    data=contract["walk"]
    env=contract["clearance_envelopes"]
    assert len(env)>=2 and all(len(x["center"])==len(x["radii"])==3 for x in env)
    assert abs(data["rise"]-.17)<1e-8 and data["sample_width"]>=2.8
    assert data["sample_headroom"]>=2.15
    assert len(data["legs"])==3
    count=0
    worst=0.0
    for leg in data["legs"]:
        start=p[leg["from"]]["foot"]
        end=p[leg["to"]]["foot"]
        steps=leg["steps"]
        assert steps>0
        assert abs(end[2]-start[2]-steps*data["rise"])<1e-7, ("landing mismatch",leg)
        dx,dy=end[0]-start[0],end[1]-start[1]
        dist=math.hypot(dx,dy)
        active_run=steps*data["run"]
        flat=(dist-active_run)/2
        assert flat>=1.5, ("no local approach/landing",leg,flat)
        tangent=[dx/dist,dy/dist]
        normal=[-tangent[1],tangent[0]]
        for i in range(251):
            t=i/250
            path_progress=max(0,min(1,(t*dist-flat)/active_run))
            foot=[start[0]+dx*t,start[1]+dy*t,
                  start[2]+steps*data["rise"]*path_progress]
            for side in [-data["sample_width"]/2,0,data["sample_width"]/2]:
                for height in [.15,1.65,data["sample_headroom"]]:
                    probe=[foot[0]+side*normal[0],foot[1]+side*normal[1],foot[2]+height]
                    score=min(envelope_value(probe,e) for e in env)
                    worst=max(score,worst)
                    assert score<=1.0,("reserved void fails",leg,round(t,3),round(score,4))
                    count+=1
    assert sum(x["steps"] for x in data["legs"])==120
    return {"route_cross_section_probes":count,"worst_reserved_void_score":round(worst,5),
            "stair_arithmetic_only":120}

def evaluate(contract):
    p=contract["programs"]
    assert list(p)==["arrival","maker","research","living"]
    assert contract["primary_hypothesis"].startswith("A:")
    active=["maker","research","living"]
    sections=contract["shared_thick_sections"]
    assert len(sections)>=3
    surface={}
    for item in sections:
        assert len(item["owners"])>=2 and len(set(item["owners"]))==len(item["owners"])
        assert set(item["owners"]).issubset(set(active))
        assert item["thickness"]>=.8
        assert 0<item["opening"][0]<item["opening"][1]<1
        patch=section_patch(item,active)
        assert patch
        surface[item["id"]]=patch
    assert any(len(x["owners_present"])==3 for x in surface.values())
    shifts={}
    for role in active:
        surviving=[x for x in sections if role in x["owners"] and len(x["owners"])>=3]
        assert surviving,("no persistent shared boundary",role)
        measurements=[]
        for s in surviving:
            base=surface[s["id"]]
            cut=section_patch(s,set(active)-{role})
            delta=max(norm(sub(a,b)) for a,b in zip(base["corners"],cut["corners"]))
            assert delta>.15,("removing activity does not reshape surviving shared section",role,s["id"],delta)
            measurements.append(round(delta,4))
        shifts[role]=max(measurements)
    portals=contract["daylight_portals"]
    assert len(portals)>=2
    dirs=[x["direction"] for x in portals]
    separation=dot(dirs[0],dirs[1])/(norm(dirs[0])*norm(dirs[1]))
    assert separation<.85,("light portals too aligned",separation)
    route=sample_walk(contract)
    return {"section_patches":surface,"shift_when_activity_removed":shifts,
            "portal_direction_cosine":round(separation,5),**route,
            "limitations":"Only abstract PRE-3D multi-owner boundary and reserved void; no physical GLB or aesthetic success"}

def main():
    source=json.loads(CONTRACT.read_text(encoding="utf-8"))
    out=evaluate(source)
    negatives={}
    for label,mutate in [
      ("break_landing",lambda x:x["programs"]["living"]["foot"].__setitem__(2,20.74)),
      ("collapse_arrival_void",lambda x:x["clearance_envelopes"][1]["radii"].__setitem__(slice(None),[.5,.5,.5])),
      ("remove_third_owner",lambda x:x["shared_thick_sections"][0]["owners"].remove("maker")),
      ("flatten_light_dirs",lambda x:x["daylight_portals"][1]["direction"].__setitem__(slice(None),x["daylight_portals"][0]["direction"]))
    ]:
        broken=copy.deepcopy(source)
        mutate(broken)
        try:
            evaluate(broken)
        except (AssertionError,KeyError,ValueError):
            negatives[label]="REJECTED"
        else:
            raise AssertionError("failed negative control: "+label)
    result={"stage":"D55 PRE-3D TEST / ART HOLD","candidate":"A exploratory only",
            "author_contract_sha256":hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "sample_route":{k:v for k,v in out.items() if k in ("route_cross_section_probes","worst_reserved_void_score","stair_arithmetic_only")},
            "shared_patch_ids":list(out["section_patches"]),
            "surviving_shared_geometry_shifts":out["shift_when_activity_removed"],
            "daylight_portal_direction_cosine":out["portal_direction_cosine"],
            "negative_tests":negatives,
            "real_glb":"NOT RUN","same_model_five_view_art":"NOT RUN",
            "real_habitable_voids":"NOT RUN","sunlight":"NOT RUN",
            "official_331_993":"NOT RUN","formal_G0_S1_G1_G2_G3":"NOT RUN",
            "art":"HOLD (not accepted)","construction":"FORBIDDEN"}
    output=ROOT/"D55_A_PRE3D_AUDIT.json"
    output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
