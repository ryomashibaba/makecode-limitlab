"""G4-C7 A9: contour entrance cut, ramp approach re-route, transfer deck relief.

Independent 3D study derived from committed A8 GLB. Y up. No Minecraft operations.
Never hide collision findings or downgrade the conservative A8 detector.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import trimesh
from g4c7_a7_portal_route import (
    world_mesh, add_deck, cylinder, DARK, box_bounds, prepared_solid,
    boolean_volume
)
from g4c7_a8_fullbody_clearance import (
    route_sweep, stitched_route, compare_views
)

ROOT_GROUND = "A7_APPROACH_CURVED_DECK"
ROOT_TRANSFER = "A8_RAMP_PROMENADE_TRANSFER_DECK"
MAIN_ARCH = "SOUTH outer load shell_A7_PORTAL"
GLAZED_ARCH = "SOUTH continuous glazed occupied band"
RAILS = {
    "Promenade rail.118","Promenade rail.119",
    "Promenade rail.240","Promenade rail.241"
}
# Independent cut into actual closed SOUTH arch band and glass, beyond A7's
# inner portal. Its Z footprint bridges the oblique approach to the arch entry.
SOUTH_FLARED_APERTURE = ((54.0,6.0,23.0),(73.0,13.1,30.0))

def approach_centerline():
    points=[]
    for i in range(81):
        u=i/80
        z=70*u
        # Keeps centerline away from former overlapping eastbound rising ramp,
        # returns smoothly to existing ramp landing at (78, 1, 70).
        x=78+9.0*math.sin(math.pi*u)**0.8
        points.append((x,1.,z))
    return points

def rebuild_a9(a8):
    expected={ROOT_GROUND,ROOT_TRANSFER,MAIN_ARCH,GLAZED_ARCH}|RAILS
    present=set(a8.graph.nodes_geometry)
    absent=expected-present
    if absent: raise AssertionError("A8 source altered, missing objects: "+str(absent))
    aperture=box_bounds(SOUTH_FLARED_APERTURE)
    modified={}
    cut_facts={}
    for name in (MAIN_ARCH,GLAZED_ARCH):
        original=prepared_solid(world_mesh(a8,name),name)
        cut_volume=boolean_volume(original,aperture)
        if cut_volume<=.1:
            raise AssertionError("A9 named structural material not physically intersected: "+name)
        cut=trimesh.boolean.difference([original,aperture],engine="manifold")
        if cut is None or cut.is_empty or not cut.is_watertight or not cut.is_volume:
            raise AssertionError("A9 aperture caused invalid material: "+name)
        modified[name+"_A9_FLARED"]=cut
        cut_facts[name]={"volume_removed":float(cut_volume),
                         "mesh_watertight":bool(cut.is_watertight),
                         "mesh_volume":bool(cut.is_volume)}
    result=trimesh.Scene()
    skipped={ROOT_GROUND,ROOT_TRANSFER,MAIN_ARCH,GLAZED_ARCH}|RAILS
    for name in a8.graph.nodes_geometry:
        if name in skipped: continue
        mat,key=a8.graph[name]
        result.add_geometry(a8.geometry[key].copy(),geom_name=name,node_name=name,
                            transform=np.array(mat))
    for name,mesh in modified.items():
        result.add_geometry(mesh,geom_name=name,node_name=name)
    # A9 copies nothing back to A8. Rebuild both bridge surfaces as real meshes.
    path=approach_centerline()
    road=add_deck(result,ROOT_GROUND,path,10.,1.12)
    assert road.is_watertight and road.is_volume
    old_start=np.array([52.,7.1,30.])
    target=np.array([55.34677322231576,6.877551020408163,30.])
    extended=[(50.65,7.17,30.)]
    extended.extend(tuple(old_start*(1-u)+target*u) for u in np.linspace(0,1,32))
    transfer=add_deck(result,ROOT_TRANSFER,extended,7.,1.20)
    assert transfer.is_watertight and transfer.is_volume
    # Two off-path raking piers frame the new oblique opening; geometrically
    # solid members, but no structural-load engineering claim.
    anchors=[
        ([72.5,.8,31.8],[66.8,16.5,31.8]),
        ([72.5,.8,14.8],[66.8,16.5,14.8])
    ]
    for i,(bottom,top) in enumerate(anchors):
        frame=cylinder(bottom,top,1.05,DARK)
        result.add_geometry(frame,geom_name="A9_FLARED_PORTAL_PIER_%s"%i,
                            node_name="A9_FLARED_PORTAL_PIER_%s"%i)
    # Railing segments were physically removed only at route access mouths.
    # This is an unfinished fall-prevention detail; no safety approval.
    facts={"aperture_bounds_xyz":SOUTH_FLARED_APERTURE,
           "removed_rail_segments":sorted(RAILS),
           "physical_material_removed":cut_facts,
           "replaced_ground_deck":ROOT_GROUND,
           "replaced_transfer_deck":ROOT_TRANSFER,
           "new_portal_piers":2,
           "new_approach_centerline_length":float(sum(
               np.linalg.norm(np.array(path[i])-np.array(path[i-1]))
               for i in range(1,len(path)))),
           "handrail_continuity":"NOT VERIFIED",
           "structural_engineering":"NOT VERIFIED"}
    return result,facts

def route_a9():
    base=stitched_route()
    rerouted=approach_centerline()
    i=0
    out=[]
    for label,pt in base:
        if label=="GROUND_APPROACH":
            out.append((label,np.asarray(rerouted[i],float)))
            i+=1
        else:
            out.append((label,np.asarray(pt,float)))
    assert i==81
    return out

def run(input_path,out):
    out.mkdir(parents=True,exist_ok=True)
    baseline=trimesh.load(input_path,force="scene")
    assert len(baseline.graph.nodes_geometry)==592, "Wrong independent A8 original"
    repaired,facts=rebuild_a9(baseline)
    route=route_a9()
    before=route_sweep(baseline,stitched_route())
    after=route_sweep(repaired,route)
    glb=out/"a9_orbital_commons_sculpted_route_study.glb"
    glb.write_bytes(repaired.export(file_type="glb"))
    (out/"a9_orbital_commons_sculpted_route_study.obj").write_text(
        repaired.export(file_type="obj"),encoding="utf8")
    reloaded=trimesh.load(glb,force="scene")
    assert len(reloaded.graph.nodes_geometry)==len(repaired.graph.nodes_geometry)
    assert np.allclose(reloaded.bounds,baseline.bounds,atol=.15),(
        reloaded.bounds,baseline.bounds)
    # Strong geometry negative controls: original A8 collides within the new
    # cut volume, the repaired named shell and glazing don't.
    cutter=box_bounds(SOUTH_FLARED_APERTURE)
    negative_before={
        n:float(boolean_volume(prepared_solid(world_mesh(baseline,n),n),cutter))
        for n in (MAIN_ARCH,GLAZED_ARCH)}
    positive_after={
        n:float(boolean_volume(prepared_solid(world_mesh(reloaded,n+"_A9_FLARED"),n),cutter))
        for n in (MAIN_ARCH,GLAZED_ARCH)}
    assert all(v>.1 for v in negative_before.values()),negative_before
    assert all(v<1.e-4 for v in positive_after.values()),positive_after
    # Never suppress remaining collisions by changing envelope dimensions.
    assert before["body_envelope"]==after["body_envelope"]
    assert after["negative_intentional_blocker_detected"]
    assert after["route_samples"]==before["route_samples"]
    # All QA outcomes are reported, whether or not the new design is better.
    compare_views(baseline,reloaded,route,out/"fourview")
    report={
      "a8_meshes":len(baseline.graph.nodes_geometry),
      "a9_meshes":len(reloaded.graph.nodes_geometry),
      "physical_changes":facts,
      "physical_corridor_negative_before":negative_before,
      "physical_corridor_positive_after":positive_after,
      "baseline_a8":{"route_samples":before["route_samples"],
          "surface_collision_samples":before["body_surface_intersection_sample_count"],
          "unsupported_foot_samples":before["unsupported_foot_samples"]},
      "a9_clearance":after,
      "differences":{
          "surface_collision_samples":after["body_surface_intersection_sample_count"]-
                     before["body_surface_intersection_sample_count"],
          "unsupported_foot_samples":after["unsupported_foot_samples"]-
                     before["unsupported_foot_samples"]},
      "art_status":"HOLD","functional_status":after["route_geometric_status"],
      "construction":"PROHIBITED","city_integration":"PROHIBITED",
      "minecraft_walk":"NOT TESTED","full_solid_containment":"NOT PROVEN",
      "private_world_data":"UNTOUCHED",
    }
    (out/"a9_sculptural_route_audit.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path(
        "artifacts/g4c7-a8/a8_orbital_commons_transfer_study.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a9"))
    args=p.parse_args()
    q=run(args.input,args.out)
    print(json.dumps({
        "meshes":[q["a8_meshes"],q["a9_meshes"]],
        "before":q["baseline_a8"],
        "surface_collision_after":q["a9_clearance"]["body_surface_intersection_sample_count"],
        "unsupported_after":q["a9_clearance"]["unsupported_foot_samples"],
        "differences":q["differences"],
        "status":q["functional_status"],"art":q["art_status"]},indent=2))
