"""Independent saved GLB audit: never imports the 3D generator. NOT art acceptance."""
from pathlib import Path
import json,hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
OUT=ROOT/"true3d_output"
D=json.loads((ROOT/"d54_spatial_contract.json").read_text(encoding="utf-8"))
def load(name):
    scene=trimesh.load(OUT/name,force="scene",process=False)
    data={}
    for n in scene.graph.nodes_geometry:
        t,k=scene.graph.get(n);m=scene.geometry[k].copy();m.apply_transform(t);data[n]=m
    return data
def ray(p,delta,meshes):
    hit=[]
    for name,m in meshes.items():
        tri=np.asarray(m.triangles,float)
        if not len(tri):continue
        e1=tri[:,1]-tri[:,0];e2=tri[:,2]-tri[:,0]
        h=np.cross(np.broadcast_to(delta,e2.shape),e2);det=np.einsum("ij,ij->i",e1,h)
        valid=abs(det)>1e-9
        inv=np.zeros_like(det);inv[valid]=1/det[valid]
        s=np.asarray(p)-tri[:,0];u=inv*np.einsum("ij,ij->i",s,h)
        q=np.cross(s,e1);v=inv*np.einsum("ij,ij->i",np.broadcast_to(delta,e2.shape),q)
        tt=inv*np.einsum("ij,ij->i",e2,q)
        if np.any(valid&(u>=0)&(v>=0)&(u+v<=1)&(tt>1e-6)&(tt<1-1e-6)):hit.append(name)
    return hit
def landing_gap(mesh):
    return float(mesh["living_deck"].bounds[1,2]-mesh["route_2_step_049"].bounds[1,2])
def shelter(mesh):
    return "maker_weather_canopy" in ray([-15,-14,5],[0,0,20],
        {k:v for k,v in mesh.items() if k=="maker_weather_canopy"})
def verify():
    a=load("D54_A_true3d.glb")
    for name in ("arrival_terrace","maker_deck","research_deck","living_deck","living_roof",
                 "living_front_left","living_front_right","living_bed","research_workbench"):
        assert name in a,("missing",name)
    step_heights=[]
    for leg,n in enumerate([20,50,50]):
        heights=[a["route_%d_step_%03d"%(leg,i)].bounds[1,2] for i in range(n)]
        assert all(abs(b-a-D["tread_rise"])<1e-5 for a,b in zip(heights,heights[1:])),("step slope",leg)
        step_heights.append(len(heights))
    assert abs(landing_gap(a))<1e-5,("unjoined living landing",landing_gap(a))
    assert shelter(a),"missing protected maker canopy"
    assert a["living_front_right"].bounds[0,0]-a["living_front_left"].bounds[1,0]>4.0
    damage=load("broken_landing.glb")
    assert abs(landing_gap(damage))>.30,"landing negative control did not trip"
    damage2=load("broken_canopy.glb")
    assert not shelter(damage2),"canopy negative control did not trip"
    blocker=load("broken_blocked.glb")
    assert "malicious_sightline_blocker" in blocker
    eye=np.asarray([-3,30,22.1]);target=np.asarray([-12,-16,5.1])
    primary={n:m for n,m in a.items() if "_rib_" in n or "transfer" in n or n.startswith("living_front")}
    original_hits=ray(eye,target-eye,primary)
    blocker_hits=ray(eye,target-eye,{"malicious_sightline_blocker":blocker["malicious_sightline_blocker"]})
    # Deliberate occlusion must actually obstruct the line, not just add a named node.
    assert blocker_hits,"sightline negative control did not obstruct"
    changes={}
    for zone in ("maker","research","living"):
        other=load("minus_"+zone+".glb")
        missing=sorted(set(a)-set(other))
        structural=[n for n in missing if n.endswith("_deck") or "_rib_" in n
                    or "canopy" in n or "transfer" in n or n.endswith("_roof")]
        assert structural,("activity deletion only removed furnishings",zone)
        changes[zone]=structural
    result={"true3d_reloaded":True,"node_count":len(a),
            "triangles":sum(len(m.faces) for m in a.values()),
            "steps":[20,50,50],"landing_delta":landing_gap(a),
            "sampled_protected_maker_canopy":shelter(a),
            "living_observation_structural_hits":original_hits,
            "malicious_sight_blocker_hits":blocker_hits,
            "negative_landing_detected":True,"negative_canopy_detected":True,
            "activity_removal_changes_actual_architecture":changes,
            "sha256":hashlib.sha256((OUT/"D54_A_true3d.glb").read_bytes()).hexdigest(),
            "actual_daylight":"NOT RUN","full_body_sweep":"NOT RUN",
            "structural_certification":"NOT RUN","weather_seal":"NOT RUN",
            "official_331_993":"NOT RUN","formal_G0_S1_G1_G2_G3":"NOT RUN",
            "art":"HOLD - human review of 5 persisted GLB renders required",
            "minecraft":"CONSTRUCTION FORBIDDEN"}
    (OUT/"independent_audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":verify()
