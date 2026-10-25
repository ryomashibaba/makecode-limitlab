"""G4-C7 A17 independent ART-FIRST research: one-piece tectonic megafolds.

Not an A16 acceptance or an engineering solution. Rebuild from persisted A13-C
and A15-B reference. Replace the TWO massive cliff envelopes only in the new
read-only art-copy with a single actual volumetric fractured megafold. Keep all
other hosted city geometry as a spatial reference. Never write Minecraft.
"""
from pathlib import Path
import argparse,json
import numpy as np
import trimesh
from PIL import Image,ImageDraw
from scipy.ndimage import gaussian_filter,label
from skimage.measure import marching_cubes
import g4c7_a7_fourview as painter
from g4c7_a8_fullbody_clearance import route_sweep
from g4c7_a9_sculptural_route import route_a9
from g4c7_a15_split_tide_urban_shells import build as a15_build, WEST,EAST,world_geometry

STEP=2.5
BOUNDS=(-125.,125.,-35.,225.,-125.,125.)
NAME="A17_MONOLITHIC_TECTONIC_CIVIC_FOLD"
FRAME_TARGET=np.array([0.,87.,0.])
FRAME_SCALE=500.

def make_monolith(mark):
    """Two fundamentally different single-body scalar fields, not four windows.

    A: ascending horizon with a north-facing canyon tear.
    B: complex concave wave-caldera with an east-opening urban rift.
    An isolated central atrium is a real missing 3D volume, not texture.
    Surface is a continuous closed GLB solid extracted from one occupied field.
    """
    assert mark in ("a","b")
    x0,x1,y0,y1,z0,z1=BOUNDS
    X,Y,Z=np.ogrid[x0:x1+STEP/2:STEP,
                   y0:y1+STEP/2:STEP,
                   z0:z1+STEP/2:STEP]
    u=(X+.16*Z)/99.
    v=(Z-.17*X)/87.
    if mark=="a":
        h=(34+111*((1+np.sin(np.pi*u/2))/2)**1.32+
           31*np.cos(np.pi*v/1.4)*np.exp(-2.4*u*u)+
           16*np.sin(2.5*np.pi*u)*np.sin(np.pi*v/1.3))
        thickness=18+20*np.exp(-1.8*u*u-.6*v*v)+8*(v+1)**2/4
        footprint=(np.abs(u)**4+.65*np.abs(v)**4)<1.05
        tear=(np.abs(u-(.02+.2*np.sin(2*v)))<(.16+.05*(v+.5)))&(v>-.10)
        pocket=((u-.52)/.23)**2+((v+.45)/.28)**2<1
        title="ASCENDING SKY-WOUND / massive open-edged civic fold"
    else:
        h=(43+95*((1+np.sin(np.pi*u/2))/2)**1.06+
           45*np.sin(np.pi*v/1.6)*np.exp(-1.8*u*u)+
           24*np.cos(2.5*np.pi*u+2*v))
        thickness=18+22*np.exp(-.9*u*u-2*v*v)+12*(u+1)**2/4
        footprint=(np.abs(u)**4+.8*np.abs(v)**4)<1.2
        tear=(np.abs(v-(.12+.25*np.sin(2.2*u)))<(.17+.04*(u+1)))&(u>-.15)
        pocket=((u+.45)/.26)**2+((v+.48)/.31)**2<1
        title="CASCADING CIVIC CALDERA / outward-opening inhabited fold"
    original=(np.abs(Y-h)<=thickness/2)&footprint&(Y>20)
    shell=original&(~tear)&(~pocket)
    labeled,n=label(shell)
    amounts=np.bincount(labeled.ravel())[1:]
    assert n==1 and amounts.max()==shell.sum(),(
        "Disconnected voxel monolith is not a unified sculpture",mark,n,
        amounts.tolist())
    lost=int(original.sum()-shell.sum())
    assert lost>=300 and lost/original.sum()>.015,(
        "Negative volume is not large enough to justify a monumental rift",
        mark,lost,original.sum())
    # A genuine saved watertight volume, no painted hole and no visual-only
    # overlay. One sampling grid is used for both candidates.
    field=gaussian_filter(shell.astype(np.float32),sigma=.55)
    vertices,faces,_,_=marching_cubes(field,.5,spacing=(STEP,STEP,STEP))
    vertices+=np.array([x0,y0,z0])
    solid=trimesh.Trimesh(vertices=vertices,faces=faces,process=True)
    solid.fix_normals()
    assert solid.is_watertight and solid.is_volume and solid.volume>200000,(
        "Invalid 3D shell",mark,solid.volume,solid.is_watertight)
    solid.visual.vertex_colors=np.tile(np.array([205,216,220,255],dtype=np.uint8),
                                       (len(solid.vertices),1))
    summary={
      "title":title,
      "pipeline":"3D occupancy field -> Gaussian iso-surface -> real closed triangular volume",
      "sampling_step_conceptual":STEP,
      "original_occupied_voxels":int(original.sum()),
      "after_true_void_occupied_voxels":int(shell.sum()),
      "void_removed_voxels":lost,
      "estimated_removed_volume_voxel_units":round(lost*STEP**3,2),
      "method_caveat":"Voxel-level negative-space measurement, NOT a manifold Boolean volume difference",
      "single_connected_occupied_component":True,
      "actual_closed_manifold":True,
      "volume_actual_mesh":round(float(solid.volume),2),
      "art_judgement":"UNAPPROVED: inspect actual four views, urban connectivity and silhouette",
      "structural_support":"NOT VERIFIED"}
    return solid,summary

def scene_from(reference,solid):
    study=trimesh.Scene()
    for name in reference.graph.nodes_geometry:
        if name in (WEST,EAST):
            continue
        study.add_geometry(world_geometry(reference,name),
                           geom_name=name,node_name=name)
    study.add_geometry(solid,geom_name=NAME,node_name=NAME)
    assert len(study.graph.nodes_geometry)==609
    return study

def four_views(a13,a15,variants,out):
    out.mkdir(parents=True,exist_ok=True)
    old_cam=dict(painter.CAMERAS)
    old_target=painter.TARGET.copy()
    old_scale=painter.SCALE
    painter.CAMERAS={v:tuple(np.asarray(cam,dtype=float)+[0.,52.,0.])
                     for v,cam in old_cam.items()}
    painter.TARGET=FRAME_TARGET.copy()
    painter.SCALE=FRAME_SCALE
    info={}
    try:
        for view,cam in painter.CAMERAS.items():
            frames=[];counts=[]
            for scene in (a13,a15,variants["a"],variants["b"]):
                img,n=painter.render(scene,view)
                frames.append(img);counts.append(n)
            w,h=painter.WIDTH,painter.HEIGHT
            sheet=Image.new("RGB",(4*w,h+42),(242,246,250))
            d=ImageDraw.Draw(sheet)
            labels=(
                "A13-C / HISTORICAL HOLD",
                "A15-B / SPLIT CLIFFS HOLD",
                "A17-A / ASCENDING SKY-WOUND HOLD",
                "A17-B / CASCADING CIVIC CALDERA HOLD")
            for i,(img,txt) in enumerate(zip(frames,labels)):
                sheet.paste(img,(i*w,42))
                d.text((i*w+10,12),txt,fill=(22,29,34))
            sheet.save(out/(view+"_a13c_a15b_a17a_a17b.png"),optimize=True)
            info[view]={"camera":list(cam),"scale":FRAME_SCALE,
                        "target":FRAME_TARGET.tolist(),"triangles":counts}
    finally:
        painter.CAMERAS=old_cam
        painter.TARGET=old_target
        painter.SCALE=old_scale
    (out/"provenance.json").write_text(json.dumps({
      "reference":"Existing persisted A13-C GLB and A15-B derived from it",
      "renderer":"Triangle-based project Pillow renderer, not Minecraft/Blender",
      "same_camera_scale_projection_per_comparison":True,
      "real_triangles_from_reloaded_GLB":True,
      "views":info},indent=2)+"\n")

def run(source_glb,out):
    out.mkdir(parents=True,exist_ok=True)
    base=trimesh.load(source_glb,force="scene")
    assert len(base.graph.nodes_geometry)==616
    original=route_sweep(base,route_a9())
    assert original["route_samples"]==331
    assert original["foot_support_samples"]==993
    assert original["body_surface_intersection_sample_count"]==45
    assert original["unsupported_foot_samples"]==0
    assert original["negative_intentional_blocker_detected"]
    ref,_=a15_build(base,"b")
    ref_path=out/"a17_a15b_reference_rebuilt.glb"
    ref_path.write_bytes(ref.export(file_type="glb"))
    ref=trimesh.load(ref_path,force="scene")
    assert len(ref.graph.nodes_geometry)==610
    records={};scenes={}
    for mark in ("a","b"):
        solid,facts=make_monolith(mark)
        new=scene_from(ref,solid)
        path=out/("a17_"+mark+"_monolithic_rift_fold.glb")
        path.write_bytes(new.export(file_type="glb"))
        (out/("a17_"+mark+"_monolithic_rift_fold.obj")).write_text(
           new.export(file_type="obj"),encoding="utf8")
        saved=trimesh.load(path,force="scene")
        assert len(saved.graph.nodes_geometry)==609
        monolith=world_geometry(saved,NAME)
        assert monolith.is_volume and monolith.is_watertight
        assert monolith.volume>200000
        qa=route_sweep(saved,route_a9())
        assert qa["route_samples"]==331
        assert qa["foot_support_samples"]==993
        assert qa["body_envelope"]==original["body_envelope"]
        assert qa["body_envelope"]["half_xz"]==.65
        assert qa["body_envelope"]["from_foot_y"]==.15
        assert qa["body_envelope"]["to_foot_y"]==3.25
        assert qa["negative_intentional_blocker_detected"]
        assert qa["body_surface_intersection_sample_count"]<=45
        assert qa["unsupported_foot_samples"]==0
        records[mark]={
          "art_concept":facts,
          "reimported_mesh_count":609,
          "bounds":np.asarray(saved.bounds).round(3).tolist(),
          "inherited_fixed_route":qa,
          "collisions_delta":qa["body_surface_intersection_sample_count"]-45,
          "unsupported_delta":qa["unsupported_foot_samples"],
          "load_transfer":"NOT VERIFIED",
          "surrounding_floor_to_new_body_joins":"NOT VERIFIED",
          "actual_walk":"NOT TESTED"}
        scenes[mark]=saved
    four_views(base,ref,scenes,out/"fourview")
    result={
      "scheme":"Radical alternative to two-cliff-with-windows morphology",
      "source_A13C_persisted_GLB_nodes":616,
      "A15B_reconstruction_nodes":610,
      "new_reimported_node_count":609,
      "omitted_original_cliff_envelopes_in_NEW_STUDY_COPY_ONLY":[WEST,EAST],
      "unchanged_old_city_world_and_research":"TRUE",
      "variants":records,
      "ART":"HOLD_PENDING_FOURVIEW",
      "MINECRAFT_CONSTRUCTION":"PROHIBITED",
      "CITY_INTEGRATION":"PROHIBITED",
      "HUMAN_ROUTE":"NOT CERTIFIED: historical 45 body surface intersections",
      "STRUCTURAL_ENGINEERING":"NOT VERIFIED",
      "historical_omitted_load_shells":"A13-C visual research copy ONLY",
      "A16_status":"INDEPENDENT: A17 is not A16 acceptance"}
    (out/"a17_geometry_qa.json").write_text(
         json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path(
       "artifacts/g4c7-a13/a13_c_unified_megafold.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a17"))
    a=p.parse_args()
    data=run(a.input,a.out)
    print(json.dumps({k:{"mesh":v["reimported_mesh_count"],
       "collisions":v["inherited_fixed_route"]["body_surface_intersection_sample_count"],
       "supports":v["inherited_fixed_route"]["unsupported_foot_samples"]}
       for k,v in data["variants"].items()},indent=2))
