"""G4-C7 A8 — real transfer deck, 3D swept-body surface clearance QA.
Read-only relative to predecessor GLBs, Minecraft, worlds, used latches.
GLB coordinates: (X, Y=up, Z). Never equate geometry with in-game walking.
"""
import argparse, json, math
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
import trimesh
from g4c7_a7_portal_route import (
    world_mesh, add_deck, cylinder, DARK, FLOOR_Y, sample_route,
    triangulated_support, support_gap
)
from g4c7_a7_fourview import render, CAMERAS, TARGET, WIDTH, HEIGHT, SCALE
from PIL import Image, ImageDraw

ROUTE_RADIUS = 0.65     # 1.30 conceptual unit across X/Z, axis-aligned envelope
HEAD_HEIGHT = 3.25     # from nominal foot plane
SOLE_OFFSET = 0.15
MAX_SAMPLE_STEP = 1.15
SUPPORT_TOLERANCE = 0.31

def attach_bridge(original):
    scene=trimesh.Scene()
    for name in original.graph.nodes_geometry:
        transform,key=original.graph[name]
        scene.add_geometry(original.geometry[key].copy(),geom_name=name,
                           node_name=name,transform=np.array(transform))
    start=np.array([52.0,7.1,30.0])
    t=math.asin(-30/49)
    finish=np.array([70*math.cos(t),13+10*math.sin(t),-49*math.sin(t)])
    delta=np.linalg.norm(finish-start)
    assert 3.0<delta<4.0,(delta,finish)
    pts=[tuple(start*(1-u)+finish*u) for u in np.linspace(0,1,25)]
    deck=add_deck(scene,"A8_RAMP_PROMENADE_TRANSFER_DECK",pts,7.0,1.2)
    assert deck.is_watertight and deck.is_volume
    for idx,u in enumerate((.23,.77)):
        p=start*(1-u)+finish*u
        for side in (-1,1):
            # Structural supports are below deck and outside the clear middle.
            z=p[2]+3.1*side
            cylinder_mesh=cylinder([p[0],.25,z],[p[0],p[1]-1,z],.42,DARK)
            scene.add_geometry(cylinder_mesh,geom_name=f"A8_TRANSFER_COLUMN_{idx}_{side}",
                                node_name=f"A8_TRANSFER_COLUMN_{idx}_{side}")
    return scene,{"endpoint_a":start.tolist(),"endpoint_b":finish.tolist(),
                  "centerline_gap_before":float(delta),
                  "bridge_mesh_watertight":bool(deck.is_watertight),
                  "bridge_mesh_volume":bool(deck.is_volume)}

def stitched_route():
    baseline=sample_route()
    sections=defaultdict(list)
    for label,pt in baseline: sections[label].append(np.array(pt,float))
    assert {n for n in sections}=={
        "GROUND_APPROACH","EXISTING_RAMP","ELLIPTICAL_LOOP","A7_PORTAL"}
    a=sections["EXISTING_RAMP"][-1]
    b=sections["ELLIPTICAL_LOOP"][0]
    route=[]
    for label in ("GROUND_APPROACH","EXISTING_RAMP"):
        route.extend((label,p) for p in sections[label])
    route.extend(("A8_TRANSFER",a*(1-u)+b*u) for u in np.linspace(1/24,1,24))
    route.extend(("ELLIPTICAL_LOOP",p) for p in sections["ELLIPTICAL_LOOP"][1:])
    route.extend(("A7_PORTAL",p) for p in sections["A7_PORTAL"])
    return route

def sat_surface_box(triangles, lo, hi):
    """Exact triangle/axis-aligned cuboid surface intersections via 13 SAT axes.
    Returns collisions, not overlap inferred from vertex centers or mesh names.
    Triangle plane, 3 AABB directions, and 9 edge x axis separation tests.
    """
    if len(triangles)==0:
        return False
    c=(lo+hi)/2
    h=(hi-lo)/2
    tri=triangles-c
    # Bounds in world axis: 3 AABB SAT axes
    active=np.ones(len(tri),dtype=bool)
    for ax in range(3):
        active &= (tri[:,:,ax].min(axis=1)<=h[ax]+1.e-8)&(
                   tri[:,:,ax].max(axis=1)>=-h[ax]-1.e-8)
    if not active.any(): return False
    tri=tri[active]
    e0=tri[:,1]-tri[:,0]
    e1=tri[:,2]-tri[:,1]
    e2=tri[:,0]-tri[:,2]
    normal=np.cross(e0,e1)
    bound=np.abs(normal)@h
    projection=np.einsum("mij,mj->mi",tri,normal)
    active=(projection.min(axis=1)<=bound+1.e-8)&(
            projection.max(axis=1)>=-bound-1.e-8)
    if not active.any():return False
    tri=tri[active]
    e0,e1,e2=e0[active],e1[active],e2[active]
    alive=np.ones(len(tri),dtype=bool)
    for edge in (e0,e1,e2):
        for direction in np.eye(3):
            axis=np.cross(edge,direction)
            p=np.einsum("mij,mj->mi",tri,axis)
            r=np.abs(axis)@h
            alive &= (p.min(axis=1)<=r+1.e-8)&(p.max(axis=1)>=-r-1.e-8)
            if not alive.any():return False
    return bool(alive.any())

def triangles_by_mesh(scene):
    out=[]
    for name in scene.graph.nodes_geometry:
        mesh=world_mesh(scene,name)
        triangles=mesh.triangles
        if len(triangles)==0:continue
        out.append((name,mesh.bounds,np.asarray(triangles,float)))
    return out

def hits_surface(prepared, lo, hi):
    collisions=[]
    for name,bounds,tri in prepared:
        if np.any(bounds[1]<lo-1e-8) or np.any(bounds[0]>hi+1e-8):
            continue
        tri_lo=tri.min(axis=1); tri_hi=tri.max(axis=1)
        candidate=np.all(tri_hi>=lo-1e-8,axis=1)&np.all(tri_lo<=hi+1e-8,axis=1)
        if not np.any(candidate):continue
        if sat_surface_box(tri[candidate],lo,hi):
            collisions.append(name)
    return collisions

def route_sweep(scene,route,full=True):
    tris=triangulated_support(scene)
    # Existing A7 support whitelist does not contain the A8 deck.
    trans=world_mesh(scene,"A8_RAMP_PROMENADE_TRANSFER_DECK")
    extra=trans.triangles
    norms=np.cross(extra[:,1]-extra[:,0],extra[:,2]-extra[:,0])
    tris=np.concatenate([tris,extra[np.abs(norms[:,1])>0.005]])
    prepared=triangles_by_mesh(scene)
    violations=[]
    gaps=[]
    group_counts=Counter()
    unsupported=[]
    checks=[]
    spacing=[]
    for idx,(label,pt) in enumerate(route):
        if idx:
            step=float(np.linalg.norm(pt-route[idx-1][1]))
            spacing.append(step)
        earlier=route[max(0,idx-1)][1]
        later=route[min(len(route)-1,idx+1)][1]
        tangent=later-earlier
        across=np.array([-tangent[2],0,tangent[0]])
        across=across/max(np.linalg.norm(across),1e-9)
        for lateral in (-.65,0.,.65):
            foot=pt+across*lateral
            gap=support_gap(tris,foot)
            if gap is None or gap<-.09 or gap>SUPPORT_TOLERANCE:
                unsupported.append({"index":idx,"section":label,
                                    "lateral":lateral,
                                    "gap":None if gap is None else round(gap,4)})
            else:gaps.append(gap)
        if not full:
            continue
        lo=pt+np.array([-ROUTE_RADIUS,SOLE_OFFSET,-ROUTE_RADIUS])
        hi=pt+np.array([ROUTE_RADIUS,HEAD_HEIGHT,ROUTE_RADIUS])
        names=hits_surface(prepared,lo,hi)
        if names:
            group_counts.update(names)
            checks.append([idx,label,*pt.tolist()])
            if len(violations)<30:
                violations.append({"index":idx,"section":label,
                                   "position":[round(float(v),3) for v in pt],
                                   "meshes":names[:15]})
    max_step=max(spacing) if spacing else 0.
    # Dedicated adversarial negative: an independently inserted AABB blocking
    # the center of the existing portal cannot escape the SAT-based check.
    p=np.array([50.,FLOOR_Y,20.])
    barrier=trimesh.creation.box(extents=[1.5,2.7,1.5])
    barrier.apply_translation([50.,FLOOR_Y+1.5,20.])
    negative=prepared+[("A8_NEGATIVE_INTENTIONAL_BLOCKER",barrier.bounds,barrier.triangles)]
    lo=p+np.array([-ROUTE_RADIUS,SOLE_OFFSET,-ROUTE_RADIUS])
    hi=p+np.array([ROUTE_RADIUS,HEAD_HEIGHT,ROUTE_RADIUS])
    negative_detected="A8_NEGATIVE_INTENTIONAL_BLOCKER" in hits_surface(negative,lo,hi)
    assert negative_detected,"Collision test failed known intentional solid blocker"
    assert max_step < MAX_SAMPLE_STEP,(max_step,"artificial teleport found")
    return {
        "route_samples":len(route),"max_adjacent_sample_step":max_step,
        "foot_support_samples":len(route)*3,
        "unsupported_foot_samples":len(unsupported),
        "unsupported_examples":unsupported[:30],
        "body_envelope":{"half_xz":ROUTE_RADIUS,"from_foot_y":SOLE_OFFSET,
                         "to_foot_y":HEAD_HEIGHT,
                         "orientation":"axis-aligned conservative square"},
        "body_surface_intersection_sample_count":len(checks),
        "per_mesh_collision_samples":dict(group_counts.most_common(50)),
        "collision_examples":violations,
        "negative_intentional_blocker_detected":negative_detected,
        "caveat":"Triangle/cuboid surface SAT is not a proof against a fully enclosed solid with no nearby surface; no voxel or in-game walking proven.",
        "route_geometric_status":
            "HOLD_SURFACE_COLLISIONS_OR_SUPPORT" if checks or unsupported
            else "SURFACE_SWEEP_CLEAR_WITH_UNTESTED_SOLID_CONTAINMENT",
    }

def compare_views(old,new,route,out):
    out.mkdir(parents=True,exist_ok=True)
    summary={}
    from g4c7_a7_fourview import CAMERAS, TARGET, WIDTH, HEIGHT, SCALE
    for view,eye0 in CAMERAS.items():
        before,n0=render(old,view)
        after,n1=render(new,view)
        eye=np.array(eye0,float); direction=TARGET-eye
        direction/=np.linalg.norm(direction)
        right=np.cross(direction,[0,1,0])
        right/=np.linalg.norm(right)
        up=np.cross(right,direction)
        draw=ImageDraw.Draw(after)
        poly=[]
        for _,pt in route:
            diff=pt-TARGET
            poly.append((WIDTH/2+float(diff@right)*WIDTH/SCALE,
                         HEIGHT/2-float(diff@up)*WIDTH/SCALE))
        draw.line(poly,fill=(239,112,29),width=3,joint="curve")
        for i in range(0,len(poly),max(1,len(poly)//30)):
            x,y=poly[i];draw.ellipse((x-3,y-3,x+3,y+3),fill=(25,50,47))
        panel=Image.new("RGB",(WIDTH*2,HEIGHT+40),(244,248,249))
        panel.paste(before,(0,40));panel.paste(after,(WIDTH,40))
        d=ImageDraw.Draw(panel)
        d.text((20,12),"A7 SOURCE - ART HOLD",fill=(15,20,24))
        d.text((WIDTH+20,12),"A8 TRANSFER + SAMPLED ROUTE - ART HOLD",fill=(15,20,24))
        panel.save(out/(view+"_a7_a8.png"),optimize=True)
        summary[view]={"a7_triangles":n0,"a8_triangles":n1,
                       "fixed_eye":list(eye0),"fixed_scale":SCALE}
    (out/"provenance.json").write_text(json.dumps({
        "renderer":"GLB-derived painter rasterization, not Blender EEVEE or Minecraft",
        "views":summary,"route_overlay":"sampled path, not walking certification"},indent=2)+"\n")

def generate(input_path,out):
    out.mkdir(parents=True,exist_ok=True)
    original=trimesh.load(input_path,force="scene")
    assert len(original.graph.nodes_geometry)==587,"Wrong A7 source"
    model,transfer=attach_bridge(original)
    route=stitched_route()
    checks=route_sweep(model,route)
    output=out/"a8_orbital_commons_transfer_study.glb"
    output.write_bytes(model.export(file_type="glb"))
    (out/"a8_orbital_commons_transfer_study.obj").write_text(
        model.export(file_type="obj"),encoding="utf8")
    fresh=trimesh.load(output,force="scene")
    assert len(fresh.graph.nodes_geometry)==len(model.graph.nodes_geometry)
    assert np.allclose(fresh.bounds,original.bounds,atol=.15)
    compare_views(original,fresh,route,out/"fourview")
    qa={"input_a7_meshes":len(original.graph.nodes_geometry),
        "result_a8_meshes":len(fresh.graph.nodes_geometry),
        "transfer":transfer,"clearance":checks,
        "art_status":"HOLD","construction":"PROHIBITED",
        "city_integration":"PROHIBITED","in_game_walk":"NOT_TESTED",
        "full_solid_containment":"NOT_PROVEN",
        "private_world_data":"UNTOUCHED"}
    (out/"a8_fullbody_clearance_qa.json").write_text(
        json.dumps(qa,ensure_ascii=False,indent=2)+"\n")
    assert checks["negative_intentional_blocker_detected"]
    return qa

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,
                   default=Path("artifacts/g4c7-a7/a7_orbital_commons_portal_study.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a8"))
    a=p.parse_args()
    r=generate(a.input,a.out)
    print(json.dumps({"meshes":[r["input_a7_meshes"],r["result_a8_meshes"]],
          "transfer_gap_before":r["transfer"]["centerline_gap_before"],
          "samples":r["clearance"]["route_samples"],
          "unsupported":r["clearance"]["unsupported_foot_samples"],
          "surface_collision_samples":r["clearance"]["body_surface_intersection_sample_count"],
          "status":r["clearance"]["route_geometric_status"]},indent=2))
