"""G4-C7 A14: inhabited tectonic braid / pure offline ART-FIRST.
Read only the exact persisted A13-C 616-geometry GLB. Neither base works nor
private Minecraft evidence are modified. No engineering or art pass is claimed.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image, ImageDraw

from g4c7_a7_fourview import CAMERAS, SCALE, WIDTH, HEIGHT, render
from g4c7_a8_fullbody_clearance import route_sweep
from g4c7_a9_sculptural_route import route_a9

SOURCE_NODES = 616
WEST = "A11_WEST_FAULT_ESCARPMENT_REAL_VOID"
EAST = "A11_EAST_SKY_FOLD_REAL_VOID"
RESEARCH_ONLY_OMISSIONS = {
    "A13_MIDDLE_INHABITED_CIVIC_FOLD",
    "A12_UPPER_UNIFIED_CIVIC_CRESCENT",
}
BRAID = "A14_INHABITED_TECTONIC_CIVIC_BRAID"
# World-space center(X,Y,Z), full width. Unlike a roof, the space-form bends
# diagonally UP, enters both banks, and returns into the middle CITY SECTION.
# Asymmetry is intentional: this is a branching public landscape, not a pipe
# resting horizontally above separate architectures.
STATIONS = [
    (-55., 23., -51., 17.), (-47., 37., -42., 19.),
    (-31., 49., -32., 23.), ( -8., 62., -20., 24.),
    ( 21., 72., -10., 19.), ( 41., 78.,   2., 15.),
    ( 48., 67.,  13., 18.), ( 31., 54.,  17., 22.),
    (  8., 45.,  21., 25.), (-20., 43.,  24., 22.),
    (-38., 47.,  15., 17.), (-47., 54.,   0., 13.),
]
COLOR=(216,211,190,255)

def cubic(p0,p1,p2,p3,t):
    return 0.5 * (2*p1 + (-p0+p2)*t +
                  (2*p0-5*p1+4*p2-p3)*t*t +
                  (-p0+3*p1-3*p2+p3)*t*t*t)

def station_curve(subdivisions=17):
    knots=np.asarray(STATIONS,dtype=float)
    result=[]
    for i in range(len(knots)-1):
        a=knots[max(0,i-1)]
        b=knots[i]
        c=knots[i+1]
        d=knots[min(len(knots)-1,i+2)]
        for j in range(subdivisions):
            result.append(cubic(a,b,c,d,j/subdivisions))
    result.append(knots[-1].copy())
    return np.asarray(result)

def single_tapered_civic_mass():
    path=station_curve()
    vertices=[]
    n=len(path)
    for i,row in enumerate(path):
        x,y,z,w=row
        left=path[max(0,i-1)]
        right=path[min(n-1,i+1)]
        tangent=(right-left)[[0,2]]
        length=np.linalg.norm(tangent)
        assert length>1e-5
        # cross-section width in plan, with irregular high ridge + carved-like
        # concave edge. Its elevated upper face is NOT a separately placed roof.
        nx,nz=-tangent[1]/length,tangent[0]/length
        u=i/(n-1)
        depth=6.4+2.0*math.sin(math.pi*u)**2
        ridge=5.0+3.0*math.sin(math.pi*u)**2
        cross=(
            (-.50,-depth),(-.47, .7*ridge),(-.15,ridge),
            ( .24, .63*ridge),(.49,-.5),(.50,-depth),
        )
        for across,up in cross:
            vertices.append((x+nx*w*across,y+up,z+nz*w*across))
    faces=[]
    sides=6
    for i in range(n-1):
        for k in range(sides):
            p=i*sides+k
            q=i*sides+(k+1)%sides
            a=(i+1)*sides+k
            b=(i+1)*sides+(k+1)%sides
            faces.extend(((p,a,b),(p,b,q)))
    end=(n-1)*sides
    for k in range(1,sides-1):
        faces.append((0,k,k+1))
        faces.append((end,end+k+1,end+k))
    mesh=trimesh.Trimesh(vertices=vertices,faces=faces,process=True)
    mesh.fix_normals()
    assert mesh.is_watertight, "A14 mass not closed"
    assert mesh.is_volume and mesh.volume>5000, "A14 no valid positive volume"
    mesh.visual=trimesh.visual.ColorVisuals(
        mesh,vertex_colors=np.tile(np.asarray(COLOR,dtype=np.uint8),
                                   (len(mesh.vertices),1)))
    return mesh

def mesh_at(scene,name):
    mat,key=scene.graph[name]
    copy=scene.geometry[key].copy()
    copy.apply_transform(np.asarray(mat))
    return copy

def build(base):
    assert len(base.graph.nodes_geometry)==SOURCE_NODES
    assert RESEARCH_ONLY_OMISSIONS.issubset(base.graph.nodes_geometry)
    assert WEST in base.graph.nodes_geometry and EAST in base.graph.nodes_geometry
    result=trimesh.Scene()
    for name in base.graph.nodes_geometry:
        if name in RESEARCH_ONLY_OMISSIONS:
            continue
        mat,key=base.graph[name]
        result.add_geometry(base.geometry[key].copy(),geom_name=name,
                            node_name=name,transform=np.asarray(mat))
    braid=single_tapered_civic_mass()
    result.add_geometry(braid,geom_name=BRAID,node_name=BRAID)
    return result,braid

def physical_intersections(base,braid):
    contacts={}
    for bank in (WEST,EAST):
        geo=mesh_at(base,bank)
        try:
            intersection=trimesh.boolean.intersection([geo,braid],engine="manifold")
            volume=0. if intersection is None or intersection.is_empty else float(intersection.volume)
            contacts[bank]={
                "measured_overlap_volume":round(volume,2),
                "is_material_overlap":bool(volume>1),
                "watertight_joint_after_union":"NOT TESTED",
                "structural_transfer":"NOT VERIFIED"
            }
        except Exception as err:
            contacts[bank]={
                "measured_overlap_volume":None,
                "is_material_overlap":"NOT VERIFIED",
                "reason":str(err)[:180],
                "structural_transfer":"NOT VERIFIED"
            }
    return contacts

def make_comparison(a12,a13c,a14,out):
    out.mkdir(parents=True,exist_ok=True)
    provenance={}
    for view,eye in CAMERAS.items():
        frames=[]
        counts=[]
        for scene in (a12,a13c,a14):
            frame,triangles=render(scene,view)
            frames.append(frame)
            counts.append(triangles)
        combined=Image.new("RGB",(WIDTH*3,HEIGHT+42),(245,247,247))
        draw=ImageDraw.Draw(combined)
        for idx,(frame,legend) in enumerate(zip(frames,(
            "A12  /  OPEN ATRIUM  /  ART HOLD",
            "A13-C  /  MID-CANYON FOLD  /  ART HOLD",
            "A14  /  TECTONIC CITY BRAID  /  ART HOLD",
        ))):
            combined.paste(frame,(idx*WIDTH,42))
            draw.text((idx*WIDTH+12,13),legend,fill=(24,29,32))
        combined.save(out/(view+"_a12_a13c_a14.png"),optimize=True)
        provenance[view]={"eye":list(eye),"scale":SCALE,"triangles":counts}
    (out/"provenance.json").write_text(json.dumps({
        "renderer":"GLB-derived orthographic Pillow painter; NOT Blender, EEVEE, Minecraft",
        "identical_reference_camera":True,
        "same_projection_scale":SCALE,
        "frames":provenance,
        "post_edit_art_judgement":"NOT CERTIFIED"
    },indent=2)+"\n")

def run(input_model,a12_model,out):
    out.mkdir(parents=True,exist_ok=True)
    source=trimesh.load(input_model,force="scene")
    ref=trimesh.load(a12_model,force="scene")
    assert len(ref.graph.nodes_geometry)==619
    assert len(source.graph.nodes_geometry)==616
    inherited=route_sweep(source,route_a9())
    assert inherited["route_samples"]==331
    assert inherited["foot_support_samples"]==993
    assert inherited["body_surface_intersection_sample_count"]==45
    assert inherited["unsupported_foot_samples"]==0
    assert inherited["negative_intentional_blocker_detected"]
    model,shape=build(source)
    output=out/"a14_tectonic_civic_braid.glb"
    output.write_bytes(model.export(file_type="glb"))
    (out/"a14_tectonic_civic_braid.obj").write_text(
        model.export(file_type="obj"),encoding="utf-8")
    persisted=trimesh.load(output,force="scene")
    assert len(persisted.graph.nodes_geometry)==615
    assert BRAID in persisted.graph.nodes_geometry
    actual_shape=mesh_at(persisted,BRAID)
    assert actual_shape.is_volume and actual_shape.is_watertight
    q=route_sweep(persisted,route_a9())
    assert q["route_samples"]==inherited["route_samples"]==331
    assert q["foot_support_samples"]==inherited["foot_support_samples"]==993
    assert q["body_envelope"]==inherited["body_envelope"]
    assert q["negative_intentional_blocker_detected"]
    assert q["body_surface_intersection_sample_count"]<=45
    assert q["unsupported_foot_samples"]==0
    contact=physical_intersections(source,actual_shape)
    make_comparison(ref,source,persisted,out/"fourview")
    report={
        "lineage":"Committed A12 -> committed A13-C -> independent A14 artistic candidate",
        "a13c_input_meshes":616,
        "a14_output_meshes":615,
        "reference_a12_meshes":619,
        "a14_real_bounds":np.asarray(persisted.bounds).round(3).tolist(),
        "new_primary_mass":{
            "node":BRAID,"real_closed_volume":round(float(actual_shape.volume),2),
            "watertight":bool(actual_shape.is_watertight),
            "valid_positive_volume":bool(actual_shape.is_volume),
            "bounds":np.asarray(actual_shape.bounds).round(3).tolist(),
            "cubic_stations":len(STATIONS),
            "art_goal":"A single rising, turning and descending urban fold between canyon banks; not a hovering roof",
            "body_vs_cliffs_real_material_overlap":contact,
            "single_boolean_fused_structure":"NOT TESTED",
            "multi-level public circulation":"NOT VERIFIED",
            "structural_loads":"NOT VERIFIED",
        },
        "visual_only_omitted_nodes":sorted(RESEARCH_ONLY_OMISSIONS),
        "historic_arch_shells":"Four omitted earlier in A13-C research copy; not structural approval",
        "old_a12_and_a13c_sources":"READ ONLY",
        "route_a13c": {
            "body_collision_samples":inherited["body_surface_intersection_sample_count"],
            "unsupported_foot_samples":inherited["unsupported_foot_samples"]},
        "route_a14":q,
        "path_collision_delta":q["body_surface_intersection_sample_count"]-45,
        "path_support_delta":q["unsupported_foot_samples"],
        "art_status":"HOLD",
        "minecraft_construction":"PROHIBITED",
        "city_integration":"PROHIBITED",
        "real_minecraft_walk":"NOT TESTED",
        "all_private_worlds_used_csv_zip":"UNTOUCHED",
        "scale_note":"Y-up research-only conceptual units, NOT Minecraft block coordinates",
        "not_certified":"Pure geometric surface checks are not holistic traversability"
    }
    (out/"a14_geometry_qa.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    return report

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,default=Path(
        "artifacts/g4c7-a13/a13_c_unified_megafold.glb"))
    parser.add_argument("--a12",type=Path,default=Path(
        "artifacts/g4c7-a12/a12_exposed_atrium_canyon.glb"))
    parser.add_argument("--out",type=Path,default=Path("build/g4c7_a14"))
    a=parser.parse_args()
    result=run(a.input,a.a12,a.out)
    print(json.dumps({
        "meshes":result["a14_output_meshes"],
        "closed_volume":result["new_primary_mass"]["real_closed_volume"],
        "contact":result["new_primary_mass"]["body_vs_cliffs_real_material_overlap"],
        "path_regressions":[result["path_collision_delta"],result["path_support_delta"]],
        "ART":result["art_status"]},indent=2))
