"""G4-C7 A15 — SPLIT-TIDE: deform the inhabited cliff architecture itself.

ART-FIRST and read-only inputs. NO Minecraft construction, engineering
approval or city integration. Two independent 3D variants with distinct
upper-contour topology; real inherited hollow cliff meshes, not added roofs.
"""
import argparse
import json
import numpy as np
import trimesh
from PIL import Image, ImageDraw
from pathlib import Path
import g4c7_a7_fourview as painter
from g4c7_a8_fullbody_clearance import route_sweep
from g4c7_a9_sculptural_route import route_a9

INPUT_NODES=616
WEST="A11_WEST_FAULT_ESCARPMENT_REAL_VOID"
EAST="A11_EAST_SKY_FOLD_REAL_VOID"
# Research-scene visibility study only. Never remove these from old GLBs/worlds.
# The four thin historic bands dominate the distant front, concealing the
# organically inhabited large negative space; the old isolated sky fold and
# cap crescent are rejected A13-style additions.
VISUAL_ONLY_OMISSIONS={
 "A13_MIDDLE_INHABITED_CIVIC_FOLD",
 "A12_UPPER_UNIFIED_CIVIC_CRESCENT",
 "NORTH continuous glazed occupied band.001",
 "NORTH continuous glazed occupied band",
 "SOUTH continuous glazed occupied band.001",
 "SOUTH continuous glazed occupied band_A9_FLARED",
}
FRONT_TARGET=np.array([0.,60.,0.])
MATCHED_SCALE=380.0

def side_of(name):
    if name.startswith(("A11_WEST","A12_WEST","A10_WEST")):return "W"
    if name.startswith(("A11_EAST","A12_EAST","A10_EAST")):return "E"
    return None

def deform_world_vertices(v,side,variant):
    """Smooth in-situ deformation, strictly identity for y<=14.

    Operates on complete original 3D solids, cavities, and hosted public
    strata simultaneously: re-sculpts the buildings, not a freestanding ribbon.
    Smoothstep creates a C1 tangent transition, preserving low-level evidence.
    """
    assert variant in ("a","b")
    v=np.asarray(v,dtype=float).copy()
    x,y,z=v.T
    t=np.clip((y-14.0)/82.0,0.0,1.0)
    s=t*t*(3.0-2.0*t)
    if variant=="a":
        # Inward-reaching reciprocal fault crests: thick, opposing spatial waves.
        lift=35*s+22*s**1.8*(.5+.5*np.sin((z+60)*.084+(0 if side=="W" else 1.7)))
        shear=(14 if side=="W" else -12)*s+(10 if side=="W" else -10)*s*s*np.sin((z+41)*.075+(0 if side=="W" else 1.5))
        twist=(24 if side=="W" else -21)*s**1.6*np.cos(.048*z+1.45)
    else:
        # Opposed outward-blooming crests; an open sky-fissure, NOT an arch.
        lift=48*s+27*s**1.6*(.5+.5*np.sin((z+60)*.09+(0 if side=="W" else 1.85)))
        shear=(21 if side=="W" else -20)*s+(-48 if side=="W" else 48)*s**2.7+(17 if side=="W" else -13)*s*s*np.sin((z+39)*.082+(.7 if side=="W" else 1.8))
        twist=(31 if side=="W" else -27)*s**1.5*np.cos(.052*z+.8)
    v[:,0]+=shear
    v[:,1]+=lift
    v[:,2]+=twist
    return v

def world_geometry(scene,node):
    mat,key=scene.graph[node]
    mesh=scene.geometry[key].copy()
    mesh.apply_transform(np.asarray(mat))
    return mesh

def build(source,variant):
    assert len(source.graph.nodes_geometry)==INPUT_NODES
    assert VISUAL_ONLY_OMISSIONS.issubset(set(source.graph.nodes_geometry))
    result=trimesh.Scene()
    changed=[]
    for node in source.graph.nodes_geometry:
        if node in VISUAL_ONLY_OMISSIONS:
            continue
        mesh=world_geometry(source,node)
        side=side_of(node)
        if side is not None:
            mesh.vertices=deform_world_vertices(mesh.vertices,side,variant)
            changed.append(node)
        result.add_geometry(mesh,geom_name=node,node_name=node)
    assert len(result.graph.nodes_geometry)==610
    assert len(changed)>=18,"Too few inhabited components deform with cliffs"
    for key in (WEST,EAST):
        m=world_geometry(result,key)
        assert m.is_watertight and m.is_volume and m.volume>75000,(
            "Lost original real hollow cliff as solid",variant,key,m.volume)
    return result,changed

def same_frame_comparison(a12,a13,variants,out):
    """Renderer from inherited project, shifted/zoomed only as one group.

    All four inputs have exactly identical projection, camera direction, target
    and scale for every view. A15 rises above the old painter's vertical crop,
    so we give ALL columns a larger fixed framing (never different zooms).
    """
    out.mkdir(parents=True,exist_ok=True)
    original_cameras=dict(painter.CAMERAS)
    original_target=painter.TARGET.copy()
    original_scale=painter.SCALE
    painter.CAMERAS={k:tuple(np.asarray(v,dtype=float)+[0.,36.,0.])
                     for k,v in original_cameras.items()}
    painter.TARGET=FRONT_TARGET.copy()
    painter.SCALE=MATCHED_SCALE
    prov={}
    try:
        for name,eye in painter.CAMERAS.items():
            frames=[];triangles=[]
            for scene in (a12,a13,variants["a"],variants["b"]):
                pic,count=painter.render(scene,name)
                frames.append(pic);triangles.append(count)
            w,h=painter.WIDTH,painter.HEIGHT
            panel=Image.new("RGB",(w*4,h+43),(245,248,249))
            legends=(
                "A12 / OLD CANYON (HOLD)",
                "A13-C / CITY FOLD (HOLD)",
                "A15-A / INWARD TIDAL SCAR (HOLD)",
                "A15-B / BLOOMING SKY FISSURE (HOLD)",
            )
            draw=ImageDraw.Draw(panel)
            for i,(frame,label) in enumerate(zip(frames,legends)):
                panel.paste(frame,(w*i,43))
                draw.text((w*i+12,12),label,fill=(30,35,37))
            panel.save(out/(name+"_a12_a13c_a15a_a15b.png"),optimize=True)
            prov[name]={"eye":list(eye),"target":FRONT_TARGET.tolist(),
                        "fixed_scale":MATCHED_SCALE,"triangles":triangles}
    finally:
        painter.CAMERAS=original_cameras
        painter.TARGET=original_target
        painter.SCALE=original_scale
    (out/"provenance.json").write_text(json.dumps({
        "source":"Actual persisted GLB and reimported A15 GLBs",
        "renderer":"Inherited Pillow orthographic triangle painter, not Blender",
        "same_camera_projection_target_scale_in_all_four_columns":True,
        "deliberately_increased_common_frame_scale_to_show_new_crests":True,
        "views":prov
    },indent=2)+"\n")

def build_and_validate(source_path,a12_path,out):
    out.mkdir(parents=True,exist_ok=True)
    base=trimesh.load(source_path,force="scene")
    reference=trimesh.load(a12_path,force="scene")
    assert len(base.graph.nodes_geometry)==616
    assert len(reference.graph.nodes_geometry)==619
    old=route_sweep(base,route_a9())
    assert old["route_samples"]==331
    assert old["foot_support_samples"]==993
    assert old["body_surface_intersection_sample_count"]==45
    assert old["unsupported_foot_samples"]==0
    assert old["negative_intentional_blocker_detected"]
    variants={};facts={};valid={}
    for mark in ("a","b"):
        scene,changed=build(base,mark)
        glb=out/("a15_"+mark+"_split_tide_urban_shells.glb")
        obj=out/("a15_"+mark+"_split_tide_urban_shells.obj")
        glb.write_bytes(scene.export(file_type="glb"))
        obj.write_text(scene.export(file_type="obj"),encoding="utf-8")
        loaded=trimesh.load(glb,force="scene")
        assert len(loaded.graph.nodes_geometry)==610
        actual=route_sweep(loaded,route_a9())
        assert actual["route_samples"]==331 and actual["foot_support_samples"]==993
        assert actual["body_envelope"]==old["body_envelope"]
        assert actual["negative_intentional_blocker_detected"]
        assert actual["body_surface_intersection_sample_count"]<=45
        assert actual["unsupported_foot_samples"]==0
        cliff_stats={}
        for node in (WEST,EAST):
            original=world_geometry(base,node)
            updated=world_geometry(loaded,node)
            assert updated.is_volume and updated.is_watertight
            assert updated.volume>75000
            cliff_stats[node]={
                "original_bounds":np.asarray(original.bounds).round(3).tolist(),
                "reloaded_bounds":np.asarray(updated.bounds).round(3).tolist(),
                "original_volume":round(float(original.volume),2),
                "deformed_real_positive_volume":round(float(updated.volume),2),
                "reloaded_closed_manifold":True,
                "original_openings_inherited":"Non-rigid deformation of prior hollow mesh",
                "new_self_intersection_proof":"NOT TESTED",
                "load_path":"NOT VERIFIED"}
        height=float(loaded.bounds[1][1])
        assert height>(135 if mark=="a" else 150)
        variants[mark]=loaded
        facts[mark]={
            "mesh_count":610,
            "genuinely_transformed_inherited_architecture":changed,
            "transformed_node_count":len(changed),
            "real_bounds":np.asarray(loaded.bounds).round(3).tolist(),
            "real_cliff_meshes":cliff_stats,
            "original_legacy_route":actual,
            "collision_delta":actual["body_surface_intersection_sample_count"]-45,
            "foot_support_delta":actual["unsupported_foot_samples"],
            "visual_observation":"UNREVIEWED_PENDING_FOURVIEW_ART_AUDIT",
            "engineering":"NOT VERIFIED",
            "free_walking":"NOT VERIFIED"}
    same_frame_comparison(reference,base,variants,out/"fourview")
    qa={
      "source_a13c_meshes":616,"source_a12_reference_meshes":619,
      "strategy":"Resculpt original inhabited hollow cliffs + attached tiers as coherent spatial organism",
      "not_roof_not_ribbon":True,
      "omitted_in_research_copy_only":sorted(VISUAL_ONLY_OMISSIONS),
      "historic_load_shell_omission":"Inherited from A13-C art copy ONLY; engineering demolition NOT AUTHORIZED",
      "source_route_collision_samples":45,
      "source_route_unsupported_foot_samples":0,
      "variants":facts,
      "art_status":"HOLD",
      "construction":"PROHIBITED",
      "city_integration":"PROHIBITED",
      "minecraft_walk":"NOT TESTED",
      "original_A5_to_A14_models_world_used_csv_zip":"UNTOUCHED",
      "new_route_and_structural_joints":"NOT VERIFIED",
      "scale":"Y-up conceptual study units, not Minecraft blocks"}
    (out/"a15_geometry_qa.json").write_text(
        json.dumps(qa,indent=2,ensure_ascii=False)+"\n")
    return qa

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path("artifacts/g4c7-a13/a13_c_unified_megafold.glb"))
    p.add_argument("--a12",type=Path,default=Path("artifacts/g4c7-a12/a12_exposed_atrium_canyon.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a15"))
    a=p.parse_args()
    q=build_and_validate(a.input,a.a12,a.out)
    print(json.dumps({"output":{k:{"meshes":v["mesh_count"],"top_y":v["real_bounds"][1][1],
        "collision_delta":v["collision_delta"],"unsupported":v["foot_support_delta"],
        "transformed":v["transformed_node_count"]} for k,v in q["variants"].items()},
        "ART":q["art_status"],"MINECRAFT":"PROHIBITED"},indent=2))
