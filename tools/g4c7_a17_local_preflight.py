"""Independent A17 preflight: reassemble 609-node city + true massive shell.

This is a fast local art-review route when GitHub Actions is backlogged. It does
NOT grant ART PASS / free walking / Minecraft use. It deliberately rebuilds
both candidate GLBs from the same committed A13-C source, then produces
same-camera A15-B/A17-A/A17-B fourviews and a strict inherited route sweep.
"""
import argparse,json
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image,ImageDraw
from g4c7_a7_fourview import render,CAMERAS
import g4c7_a7_fourview as painter
from g4c7_a8_fullbody_clearance import route_sweep
from g4c7_a9_sculptural_route import route_a9
from g4c7_a15_split_tide_urban_shells import build as a15_build
from g4c7_a17_monolithic_rift_fold import make_monolith,scene_from,NAME

# Input is a real persisted reference, not a prompt-image approximation.
COMPARISON_TARGET=np.array([0.,82.,0.])
COMPARISON_SCALE=510.
LOOK={
    "front":(0.,102.,350.),
    "oblique":(270.,225.,330.),
    "side":(350.,109.,0.),
    "aerial":(150.,425.,135.),
}


def draw_reality(ref,variants,out):
    out.mkdir(parents=True,exist_ok=True)
    oldc=dict(painter.CAMERAS);oldt=painter.TARGET.copy();olds=painter.SCALE
    painter.CAMERAS=LOOK.copy()
    painter.TARGET=COMPARISON_TARGET.copy()
    painter.SCALE=COMPARISON_SCALE
    details={}
    try:
        for view in LOOK:
            frames=[];triangles=[]
            for scene in (ref,variants["a"],variants["b"]):
                im,n=painter.render(scene,view)
                frames.append(im);triangles.append(n)
            w,h=painter.WIDTH,painter.HEIGHT
            panel=Image.new("RGB",(w*3,h+40),(241,246,249))
            d=ImageDraw.Draw(panel)
            for i,(im,title) in enumerate(zip(frames,(
                "A15-B / REAL CLIFFS (HOLD)",
                "A17-A / REAL WOUNDED FOLD (ART REJECT)",
                "A17-B / REAL CALDERA (ART REJECT)"
            ))):
                panel.paste(im,(w*i,40))
                d.text((w*i+10,12),title,fill=(28,35,41))
            panel.save(out/(view+"_a15b_a17a_a17b.png"),optimize=True)
            details[view]={"camera":list(LOOK[view]),"triangles":triangles,
                "target":COMPARISON_TARGET.tolist(),"scale":COMPARISON_SCALE}
    finally:
        painter.CAMERAS=oldc;painter.TARGET=oldt;painter.SCALE=olds
    (out/"provenance.json").write_text(json.dumps({
        "mode":"independent GLB-reloaded art review, NOT a Minecraft render",
        "same_camera_scale_projection_in_each_comparison":True,
        "art_judgement":"REJECT_A_AND_B_ART_HOLD",
        "views":details
    },indent=2)+"\n")


def run(input_glb,out):
    out.mkdir(parents=True,exist_ok=True)
    base=trimesh.load(input_glb,force="scene")
    assert len(base.graph.nodes_geometry)==616
    old=route_sweep(base,route_a9())
    assert old["route_samples"]==331
    assert old["foot_support_samples"]==993
    assert old["body_surface_intersection_sample_count"]==45
    assert old["unsupported_foot_samples"]==0
    assert old["negative_intentional_blocker_detected"]
    a15,_=a15_build(base,"b")
    reference=out/"a17_preflight_reference_a15b.glb"
    reference.write_bytes(a15.export(file_type="glb"))
    a15=trimesh.load(reference,force="scene")
    assert len(a15.graph.nodes_geometry)==610
    results={};candidates={}
    for mode in "ab":
        solid,info=make_monolith(mode)
        scene=scene_from(a15,solid)
        p=out/("a17_"+mode+"_preflight_full_city.glb")
        p.write_bytes(scene.export(file_type="glb"))
        reload=trimesh.load(p,force="scene")
        assert len(reload.graph.nodes_geometry)==609
        # A geometrically closed mass does not prove physical connection.
        q=route_sweep(reload,route_a9())
        assert q["route_samples"]==331
        assert q["foot_support_samples"]==993
        assert q["body_envelope"]==old["body_envelope"]
        assert q["negative_intentional_blocker_detected"]
        assert q["unsupported_foot_samples"]==0
        assert q["body_surface_intersection_sample_count"]<=45
        assert info["actual_closed_manifold"]
        results[mode]={
            "mass_real_volume":info["volume_actual_mesh"],
            "grid_removed_real_occupancy":info["void_removed_voxels"],
            "full_GL B_scene_nodes".replace(" ",""):609,
            "inherited_route_331_993":q,
            "art_judgement":"REJECT/HOLD",
            "historic_load_shells":"NOT REENGINEERED",
            "upper_city_joins":"NOT VERIFIED",
            "actual_walking":"NOT VERIFIED",
            "Minecraft_construction":"PROHIBITED"}
        candidates[mode]=reload
    draw_reality(a15,candidates,out/"fourview")
    report={
        "source_A13C_persisted_GL B".replace(" ",""):str(input_glb),
        "source_original_unchanged":True,
        "input_legacy_collision_count":45,
        "original_foot_support_failures":0,
        "variants":results,
        "geometry_and_art_decision_distinct":True,
        "art":"REJECT/HOLD",
        "city_integration":"PROHIBITED",
        "Minecraft_construction":"PROHIBITED"}
    (out/"preflight_reconstruction_qa.json").write_text(json.dumps(
        report,indent=2,ensure_ascii=False)+"\n")
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--input",type=Path,
        default=Path("artifacts/g4c7-a13/a13_c_unified_megafold.glb"))
    parser.add_argument("--out",type=Path,
        default=Path("build/g4c7_a17_local_preflight"))
    args=parser.parse_args()
    result=run(args.input,args.out)
    print(json.dumps({
        k:{"collisions":v["inherited_route_331_993"]["body_surface_intersection_sample_count"],
           "unsupported":v["inherited_route_331_993"]["unsupported_foot_samples"]}
        for k,v in result["variants"].items()},indent=2))
