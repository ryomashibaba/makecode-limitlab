"""G4-C7 A11 — opposed inhabited sky-fault cliffs, NOT Minecraft construction.

Architectural, ART-FIRST counter-study to A10's pod-like silhouette. Input is
the actual generated A10 GLB; the A9/A10 lineage and worlds remain untouched.
Y is up; dimensions are conceptual model units, not validated Minecraft blocks.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image, ImageDraw

from g4c7_a7_portal_route import add_deck, box_bounds
from g4c7_a7_fourview import CAMERAS, TARGET, SCALE, WIDTH, HEIGHT, render
from g4c7_a8_fullbody_clearance import route_sweep
from g4c7_a9_sculptural_route import route_a9
from g4c7_a10_inhabited_double_canyon import swept_prism

LEFT = "A11_WEST_FAULT_ESCARPMENT_REAL_VOID"
RIGHT = "A11_EAST_SKY_FOLD_REAL_VOID"
STONE = (223,229,217,255)
DARK = (85,117,124,255)
PALE = (174,202,194,255)
WARM = (179,145,107,255)
EXPECTED_A10_MESHES=602

def add(scene,mesh,name,rgba):
    if not mesh.is_watertight or not mesh.is_volume:
        raise AssertionError("Non-manifold/cliff is not volume: "+name)
    mesh.visual=trimesh.visual.ColorVisuals(mesh,vertex_colors=np.tile(rgba,(len(mesh.vertices),1)))
    scene.add_geometry(mesh,geom_name=name,node_name=name)
    return mesh

def cliff_section(which,t):
    west=(which=="WEST")
    z=(-61.0 if west else -60.0)+(86.0 if west else 76.0)*t
    amp=math.sin(math.pi*t)**2
    if west:
        bottomx=-52+5.5*math.sin(1.8*math.pi*t-0.3)
        topx=-31+11.5*math.sin(1.65*math.pi*t+0.3)
        topy=74+7*t+10*amp
        bw=23.0+4*amp
        tw=16.5+2*amp
    else:
        bottomx=50.5+4.2*math.sin(2.3*math.pi*t+0.65)
        topx=28.0+7.8*math.sin(1.7*math.pi*t+1.2)
        topy=84-5*t+10*amp
        bw=24.0+3*amp
        tw=14.5+4*amp
    # Each asymmetric polyhedral ring forms a rock-like artificial escarpment:
    # broad inhabited foundation and strongly inward-cantilevered fractured crest.
    contour=[
      (bottomx-bw/2,0.3),
      (bottomx+bw/2,0.3),
      (bottomx+bw/2+2.2,15.0),
      (topx+tw/2+2.0,topy-16.0),
      (topx+tw/2-1.2,topy),
      (topx-tw/2,topy+2.5),
      (topx-tw/2-2.5,topy-9.0),
      (bottomx-bw/2-2.0,17.0),
    ]
    return z,contour,{"bottom_x":bottomx,"top_x":topx,"crest_y":topy+2.5,"width":bw}

def loft_cliff(which,stations=88):
    rings=[cliff_section(which,i/stations) for i in range(stations+1)]
    count=len(rings[0][1])
    vertices=np.array([[x,y,z] for z,profile,_ in rings for x,y in profile],dtype=float)
    faces=[]
    for i in range(len(rings)-1):
        a=count*i;b=count*(i+1)
        for k in range(count):
            q=(k+1)%count
            faces.extend(((a+k,b+k,b+q),(a+k,b+q,a+q)))
    last=(len(rings)-1)*count
    for k in range(1,count-1):
        faces.append((0,k,k+1))
        faces.append((last,last+k+1,last+k))
    m=trimesh.Trimesh(vertices=vertices,faces=faces,process=True)
    m.fix_normals()
    if not m.is_volume and m.is_watertight:
        m.invert()
    if not m.is_volume or not m.is_watertight:
        raise AssertionError("Actual monolithic cliff loft invalid")
    return m,rings

def carve(real,which,rings):
    """Manifold excavation: longitudinal hollow gallery and broad true mouths."""
    west=(which=="WEST")
    void_rows=[]
    # Continuous deep, inhabitable VOLUME opening from BOTH cliff ends.
    for z,contour,state in rings:
        # Interior aligns with the leaning center of the thick artificial wall.
        innerx=state["bottom_x"]*.52+state["top_x"]*.48
        roof=(60 if west else 66)+3.8*math.sin((z+60)/85*math.pi)**2
        void_rows.append((innerx,roof,z,8.6,19.0))
    passage=swept_prism(void_rows,inset_width=0.,extend_ends=3.5)
    overlap=trimesh.boolean.intersection([real,passage],engine="manifold")
    evacuated=float(overlap.volume) if overlap is not None else 0.
    if evacuated < 600:
        raise AssertionError("Genuine interior evacuation absent: "+which+" "+str(evacuated))
    shell=trimesh.boolean.difference([real,passage],engine="manifold")
    if shell is None or shell.is_empty or not shell.is_watertight or not shell.is_volume:
        raise AssertionError("Cliff failed hollow excavation: "+which)
    mouths=[]
    for zcenter,center_y in ((-39.,41.),(-7.,49.)):
        cutter=trimesh.creation.box(extents=(145.,13.0,11.0))
        cutter.apply_translation([0.,center_y,zcenter])
        intersection=trimesh.boolean.intersection([shell,cutter],engine="manifold")
        removed=float(intersection.volume) if intersection is not None else 0.
        if removed<10:
            raise AssertionError("Carved canyon aperture missed cliff: "+which)
        revised=trimesh.boolean.difference([shell,cutter],engine="manifold")
        if revised is None or revised.is_empty or not revised.is_watertight or not revised.is_volume:
            raise AssertionError("Massive aperture made non-manifold cliff")
        shell=revised
        mouths.append({"z":zcenter,"y":center_y,"removed_volume":round(removed,2)})
    return shell,{"raw_volume":round(real.volume,1),
                  "physical_void_removed":round(evacuated,1),
                  "void_ratio":round(evacuated/real.volume,4),
                  "cut_through_mouths":mouths,
                  "contains_real_longitudinal_cavity":True,
                  "cavity_walking":"NOT VERIFIED",
                  "structural_loads":"NOT VERIFIED",
                  "bounds":np.asarray(shell.bounds).round(3).tolist()}

def terraces(scene,which):
    """Three thick inhabited strata per cliff, not thin repeated balconies."""
    west=(which=="WEST")
    out=[]
    for tier,(z0,z1,ybase,width) in enumerate((
      (-52.,-12.,25.0,12.8),
      (-37.,0.,38.0,11.5),
      (-16.,16.,58.0,9.7),
    )):
        points=[]
        for i in range(45):
            u=i/44
            z=z0+(z1-z0)*u
            t=(z+(61 if west else 60))/(86 if west else 76)
            t=max(0.,min(1.,t))
            _,_,state=cliff_section(which,t)
            inward=state["bottom_x"]+(12 if west else -12)
            x=inward+(4.2 if west else -4.2)*math.sin(math.pi*u)**2
            y=ybase+3.5*math.sin(math.pi*u)**2+1.0*u
            points.append((x,y,z))
        label=("A11_WEST" if west else "A11_EAST")+"_OCCUPIED_STRATUM_"+str(tier)
        mesh=add_deck(scene,label,points,width=width,depth=3.1+0.3*tier,rgba=WARM if tier==1 else PALE)
        if not mesh.is_volume or not mesh.is_watertight:
            raise AssertionError("Urban canyon thick stratum invalid")
        out.append({"name":label,"volume":round(float(mesh.volume),1),
                    "continuous_from_ground":"NOT VERIFIED"})
    return out

def cross_bridges(scene):
    # Two different-height connecting sky corridors with broad, sculptural
    # gravity-like weight; they visibly stitch the two artificial escarpments.
    out=[]
    for label,z0,y0,swerve,width in (
      ("A11_LOW_FAULT_SKY_BOULEVARD",-28.,47.0,-6.0,11.0),
      ("A11_HIGH_CREST_TRANSECT",5.,65.0,8.0,9.0)
    ):
        points=[]
        for i in range(73):
            u=i/72
            x=-39.0+78.0*u
            y=y0+4.5*math.sin(math.pi*u)**2+3.0*u
            z=z0+swerve*math.sin(math.pi*u)+3.0*math.sin(2*math.pi*u)
            points.append((x,y,z))
        mesh=add_deck(scene,label,points,width=width,depth=5.4,rgba=STONE)
        if not mesh.is_volume or not mesh.is_watertight:
            raise AssertionError("Sky-boulevard is not a real solid")
        out.append({"name":label,"mesh_volume":round(mesh.volume,2),
                    "connections_to_cavities":"NOT VERIFIED"})
    return out

def build(source):
    result=trimesh.Scene()
    for name in source.graph.nodes_geometry:
        matrix,key=source.graph[name]
        result.add_geometry(source.geometry[key].copy(),geom_name=name,
                            node_name=name,transform=np.asarray(matrix))
    forms={}
    for which,label in (("WEST",LEFT),("EAST",RIGHT)):
        raw,rings=loft_cliff(which)
        shell,stats=carve(raw,which,rings)
        add(result,shell,label,STONE if which=="WEST" else PALE)
        stats["inhabited_terraces"]=terraces(result,which)
        forms[which.lower()]=stats
    forms["sky_boulevards"]=cross_bridges(result)
    return result,forms

def render_views(a10,a11,out):
    out.mkdir(parents=True,exist_ok=True)
    summary={}
    for v,camera in CAMERAS.items():
        before,na=render(a10,v)
        after,nb=render(a11,v)
        panel=Image.new("RGB",(2*WIDTH,HEIGHT+40),(247,248,249))
        panel.paste(before,(0,40));panel.paste(after,(WIDTH,40))
        p=ImageDraw.Draw(panel)
        p.text((20,10),"A10 HOLLOW PODS / ART HOLD",fill=(18,29,31))
        p.text((WIDTH+20,10),"A11 MEGAFISSURE CITY CLIFFS / ART HOLD",fill=(18,29,31))
        panel.save(out/(v+"_a10_a11.png"),optimize=True)
        summary[v]={"unchanged_camera":list(camera),"unchanged_scale":SCALE,
                    "a10_triangles":na,"a11_triangles":nb}
        # Identical crop for both studies, clearly labeled DETAIL and not a
        # new camera/render or a deceptive independent scale.
        if v=="oblique":
            crop=(145,130,815,635)
            pane=Image.new("RGB",(2*WIDTH,HEIGHT+40),(247,248,249))
            for i,im in enumerate((before,after)):
                detail=im.crop(crop).resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
                pane.paste(detail,(i*WIDTH,40))
            q=ImageDraw.Draw(pane)
            q.text((20,10),"A10 DETAIL (FIXED CROP) / HOLD",fill=(18,29,31))
            q.text((WIDTH+20,10),"A11 DETAIL (EXACT SAME CROP) / HOLD",fill=(18,29,31))
            pane.save(out/"oblique_detail_a10_a11.png",optimize=True)
            summary["oblique_detail"]={"source_view":v,"same_crop_xyxy":list(crop)}
    (out/"provenance.json").write_text(json.dumps({
        "source":"Actual GLB mesh triangles; not generated illustration",
        "renderer":"Pillow orthographic polygon painter; not Blender EEVEE or game capture",
        "fixed_target":TARGET.tolist(),"views":summary},indent=2)+"\n")

def generate(input_a10,out):
    out.mkdir(parents=True,exist_ok=True)
    origin=trimesh.load(input_a10,force="scene")
    if len(origin.graph.nodes_geometry)!=EXPECTED_A10_MESHES:
        raise AssertionError("A11 source must be proven 602-mesh A10")
    new,forms=build(origin)
    output=out/"a11_megafissure_inhabited_cliffs.glb"
    output.write_bytes(new.export(file_type="glb"))
    (out/"a11_megafissure_inhabited_cliffs.obj").write_text(
        new.export(file_type="obj"),encoding="utf-8")
    check=trimesh.load(output,force="scene")
    if len(check.graph.nodes_geometry)!=len(new.graph.nodes_geometry):
        raise AssertionError("GLB reload lost named geometry")
    route=route_a9()
    baseline=route_sweep(origin,route)
    actual=route_sweep(check,route)
    if baseline["body_envelope"]!=actual["body_envelope"]:
        raise AssertionError("QA tolerances were weakened")
    if baseline["route_samples"]!=actual["route_samples"] or actual["route_samples"]!=331:
        raise AssertionError("QA sampling changed")
    if actual["negative_intentional_blocker_detected"]!=True:
        raise AssertionError("Negative control failed")
    render_views(origin,check,out/"fourview")
    qa={"lineage":"A9->A10->A11 independent visual research",
        "a10_input_meshes":len(origin.graph.nodes_geometry),
        "a11_output_meshes":len(check.graph.nodes_geometry),
        "a10_bounds":np.asarray(origin.bounds).round(3).tolist(),
        "a11_bounds":np.asarray(check.bounds).round(3).tolist(),
        "tall_canyon_forms":forms,
        "a10_route":{"surface_collision_samples":baseline["body_surface_intersection_sample_count"],
                     "unsupported_foot_samples":baseline["unsupported_foot_samples"]},
        "a11_route":actual,
        "collision_delta":actual["body_surface_intersection_sample_count"]-
                          baseline["body_surface_intersection_sample_count"],
        "support_delta":actual["unsupported_foot_samples"]-
                        baseline["unsupported_foot_samples"],
        "art_status":"HOLD","construction":"PROHIBITED",
        "city_integration":"PROHIBITED","in_game_walking":"NOT TESTED",
        "upper_cavity_walking":"NOT TESTED","structural_engineering":"NOT VERIFIED",
        "private_world_or_latch":"UNTOUCHED",
        "height_note":"New research form can exceed former 66-unit study bound: ART-FIRST only"}
    (out/"a11_art_geometry_qa.json").write_text(
        json.dumps(qa,indent=2,ensure_ascii=False)+"\n")
    return qa

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path(
        "build/g4c7_a10/a10_inhabited_double_shell_canyon.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a11"))
    x=p.parse_args()
    qa=generate(x.input,x.out)
    print(json.dumps({"a10":qa["a10_input_meshes"],
                      "a11":qa["a11_output_meshes"],
                      "height":qa["a11_bounds"][1][1],
                      "a10_route":qa["a10_route"],
                      "a11_route":{"collision":qa["a11_route"]["body_surface_intersection_sample_count"],
                                   "support_failures":qa["a11_route"]["unsupported_foot_samples"]},
                      "ART":"HOLD"},indent=2))
