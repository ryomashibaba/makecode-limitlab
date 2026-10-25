"""G4-C7 A12 — exposed atrium canyon, actual volume Boolean excavation.

Art-first follow-up to A11 B2. Load the *committed* actual 613-mesh A11 GLB,
not regenerated predecessors, preserve original branch and private Minecraft
worlds. Add asymmetric, vaulted exterior-visible atria plus real public floor
volumes. All new routes and structural engineering remain NOT VERIFIED.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image, ImageDraw

from g4c7_a7_portal_route import add_deck
from g4c7_a7_fourview import render, CAMERAS, TARGET, WIDTH, HEIGHT, SCALE
from g4c7_a8_fullbody_clearance import route_sweep
from g4c7_a9_sculptural_route import route_a9

WEST="A11_WEST_FAULT_ESCARPMENT_REAL_VOID"
EAST="A11_EAST_SKY_FOLD_REAL_VOID"
INPUT_MESHES=613
CUTTERS=[
    # Name, source mass, concept center(X,Y,Z), ellipsoid radii X/Y/Z.
    # Large unequal apertures expose the genuinely inhabited inner structure
    # and are deliberately not rhythmically repeated rectangular windows.
    ("A12_WEST_GRAND_HOLLOW", WEST, (-31.0,44.0,-25.0),(25.0,17.0,23.0)),
    ("A12_WEST_SKY_OCULUS",WEST,(-21.0,72.0,1.5),(19.0,11.0,16.0)),
    ("A12_EAST_BASE_ATRIUM",EAST,(53.0,34.0,-40.0),(21.0,12.0,17.0)),
    ("A12_EAST_CROSS_ATRIUM",EAST,(44.0,53.0,-18.0),(24.0,16.0,21.0)),
    ("A12_EAST_CROWN_OCULUS",EAST,(32.0,76.0,1.0),(17.0,11.0,13.0)),
]
FLOOR_MATERIAL=(178,203,196,255)
HIGH_SKY_MATERIAL=(193,172,138,255)

def world_mesh(scene,node):
    transform,key=scene.graph[node]
    item=scene.geometry[key].copy()
    item.apply_transform(np.asarray(transform))
    return item

def body(name,geom):
    if geom is None or geom.is_empty:
        raise AssertionError("Empty model output: "+name)
    geom.fix_normals()
    if not geom.is_watertight or not geom.is_volume or geom.volume<=0:
        raise AssertionError("A12 surface is not a valid sealed volume: "+name)
    return geom

def ellipsoid(center,radii):
    # A physically closed non-rectangular arch/oculus cutting tool.
    tool=trimesh.creation.icosphere(subdivisions=3)
    tool.apply_scale(np.asarray(radii,float))
    tool.apply_translation(np.asarray(center,float))
    return body("CURVED_CUTTER",tool)

def new_scene_copy(source,overrides):
    result=trimesh.Scene()
    for name in source.graph.nodes_geometry:
        if name in overrides:
            result.add_geometry(overrides[name],geom_name=name,node_name=name)
        else:
            transform,key=source.graph[name]
            result.add_geometry(source.geometry[key].copy(),geom_name=name,
                                node_name=name,transform=np.asarray(transform))
    return result

def carve_original_cliffs(source):
    outcomes={}
    new_meshes={}
    for mass in (WEST,EAST):
        g=body(mass,world_mesh(source,mass))
        before=float(g.volume)
        slots=[]
        for name,source_name,center,radii in CUTTERS:
            if source_name!=mass:continue
            cuttool=ellipsoid(center,radii)
            common=trimesh.boolean.intersection([g,cuttool],engine="manifold")
            removed=float(common.volume) if common is not None else 0.
            if removed<120:
                raise AssertionError("A12 atrium has no real substantial cut: "+
                                     name+" measured "+str(removed))
            nextg=trimesh.boolean.difference([g,cuttool],engine="manifold")
            g=body(mass+" after "+name,nextg)
            slots.append({"name":name,
                          "nominal_ellipsoid_center":center,
                          "nominal_ellipsoid_radii":radii,
                          "real_removed_volume":round(removed,2),
                          "volume_still_closed":bool(g.is_watertight)})
        new_meshes[mass]=g
        outcomes[mass]={
            "base_real_volume":round(before,2),
            "final_real_volume":round(float(g.volume),2),
            "additional_ellipsoid_excavated_volume":round(before-float(g.volume),2),
            "real_exposed_atria":slots,
            "reconstruction":"Manifold Boolean difference on original B2 cliff",
            "upper_gallery_walking":"NOT VERIFIED",
        }
    return new_meshes,outcomes

def inhabited_shelves(scene):
    """Thick platforms visibly suspended in the carved volumes, not signage.

    Positions originate from the literal cutter. This creates *real geometry*
    and a concept gallery. Ground access/egress and anti-fall railings absent.
    """
    items=[]
    for name,_,center,radii in CUTTERS:
        x,y,z=center;rx,ry,rz=radii
        rows=[]
        height=y-ry*.30
        for i in range(35):
            u=i/34
            z0=z+(u-.5)*rz*.97
            xx=x+2.1*math.sin(math.pi*u)**2
            yy=height+1.1*math.sin(math.pi*u)**2
            rows.append((xx,yy,z0))
        newname=name+"_EXPOSED_CIVIC_DECK"
        deck=add_deck(scene,newname,rows,width=min(18.0,rx*1.15),
                      depth=3.2,rgba=FLOOR_MATERIAL)
        body(newname,deck)
        items.append({"name":newname,"volume":round(float(deck.volume),2),
                      "visitor_access":"NOT VERIFIED",
                      "railing":"NOT VERIFIED"})
    return items

def upper_canyon_crescent(scene):
    """One prominent traversing roof-level mass visually joins opposed crests.

    Not represented as a safe/continuous pedestrian route.
    """
    path=[]
    for i in range(77):
        u=i/76.
        x=-36+71*u
        y=72.0+7.2*math.sin(math.pi*u)**2+1.4*u
        z=-16+12.5*math.sin(math.pi*u)**2+3.0*math.sin(2*math.pi*u)
        path.append((x,y,z))
    name="A12_UPPER_UNIFIED_CIVIC_CRESCENT"
    mesh=add_deck(scene,name,path,width=12.0,depth=6.0,
                  rgba=HIGH_SKY_MATERIAL)
    body(name,mesh)
    return {"name":name,"real_solid_volume":round(float(mesh.volume),2),
            "ends_attached_to_core":"NOT VERIFIED",
            "upper_level_walking":"NOT VERIFIED",
            "maximum_centerline_height":max(p[1] for p in path)}

def make_views(old,new,out):
    out.mkdir(parents=True,exist_ok=True)
    meta={}
    for view,camera in CAMERAS.items():
        a,na=render(old,view)
        b,nb=render(new,view)
        pair=Image.new("RGB",(WIDTH*2,HEIGHT+38),(246,249,248))
        pair.paste(a,(0,38));pair.paste(b,(WIDTH,38))
        d=ImageDraw.Draw(pair)
        d.text((20,10),"A11 B2 SKY FAULT / ART HOLD",fill=(24,33,36))
        d.text((WIDTH+20,10),"A12 REAL EXPOSED ATRIUM CANYON / ART HOLD",fill=(24,33,36))
        pair.save(out/(view+"_a11_a12.png"),optimize=True)
        meta[view]={"camera":list(camera),"scale":SCALE,
                    "source_triangle_count":na,"new_triangle_count":nb}
    (out/"image_provenance.json").write_text(json.dumps({
        "source":"Actual committed GLB meshes",
        "renderer":"Pillow triangle orthographic painter, not EEVEE or Minecraft",
        "same_camera_target":TARGET.tolist(),"fixed_scale":SCALE,
        "views":meta},indent=2)+"\n",encoding="utf8")

def generate(input_model,out):
    out.mkdir(parents=True,exist_ok=True)
    source=trimesh.load(input_model,force="scene")
    assert len(source.graph.nodes_geometry)==INPUT_MESHES, "Not latest verified A11 B2"
    replacements,cuts=carve_original_cliffs(source)
    combined=new_scene_copy(source,replacements)
    shelves=inhabited_shelves(combined)
    crescent=upper_canyon_crescent(combined)
    path=out/"a12_exposed_atrium_canyon.glb"
    path.write_bytes(combined.export(file_type="glb"))
    (out/"a12_exposed_atrium_canyon.obj").write_text(
        combined.export(file_type="obj"),encoding="utf8")
    final=trimesh.load(path,force="scene")
    if len(final.graph.nodes_geometry)!=len(combined.graph.nodes_geometry):
        raise AssertionError("GLB damaged by export/reload")
    assert len(final.graph.nodes_geometry)==INPUT_MESHES+len(shelves)+1
    # Prove the new stored model still contains actual valid material.
    persisted={}
    for mass in (WEST,EAST):
        m=body(mass+" reloaded",world_mesh(final,mass))
        persisted[mass]={"watertight":bool(m.is_watertight),
                         "real_volume":round(float(m.volume),2)}
        if m.volume>=cuts[mass]["base_real_volume"]-100:
            raise AssertionError("A12 true volume removal not persisted: "+mass)
    route=route_a9()
    before=route_sweep(source,route)
    after=route_sweep(final,route)
    assert before["body_envelope"]==after["body_envelope"]
    assert before["route_samples"]==after["route_samples"]==331
    assert before["foot_support_samples"]==after["foot_support_samples"]==993
    assert after["negative_intentional_blocker_detected"]
    make_views(source,final,out/"fourview")
    report={
      "a11_input_meshes":len(source.graph.nodes_geometry),
      "a12_output_meshes":len(final.graph.nodes_geometry),
      "cliff_excavation":cuts,
      "persisted_cliff_volume":persisted,
      "inhabited_public_shelves":shelves,
      "sky_crescent":crescent,
      "a11_route":{"body_collision_samples":
                   before["body_surface_intersection_sample_count"],
                   "unsupported_foot_samples":before["unsupported_foot_samples"]},
      "a12_route":after,
      "collision_delta":after["body_surface_intersection_sample_count"]-
                         before["body_surface_intersection_sample_count"],
      "support_delta":after["unsupported_foot_samples"]-
                      before["unsupported_foot_samples"],
      "beyond_existing_route":"NOT TESTED",
      "interior_architecture":"UNVERIFIED FOR PUBLIC ACCESS",
      "aesthetic_approval":"HOLD","construction":"PROHIBITED",
      "city_integration":"PROHIBITED","minecraft_walk":"NOT TESTED",
      "private_world_legacy":"UNTOUCHED",
    }
    (out/"a12_exposed_atrium_geometry_qa.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path(
        "artifacts/g4c7-a11/a11_megafissure_inhabited_cliffs.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a12"))
    args=p.parse_args()
    q=generate(args.input,args.out)
    print(json.dumps({
      "input_meshes":q["a11_input_meshes"],
      "output_meshes":q["a12_output_meshes"],
      "west_removed":q["cliff_excavation"][WEST]["additional_ellipsoid_excavated_volume"],
      "east_removed":q["cliff_excavation"][EAST]["additional_ellipsoid_excavated_volume"],
      "body_collisions":[q["a11_route"]["body_collision_samples"],
                         q["a12_route"]["body_surface_intersection_sample_count"]],
      "unsupported":[q["a11_route"]["unsupported_foot_samples"],
                     q["a12_route"]["unsupported_foot_samples"]],
      "art":"HOLD"},indent=2))
