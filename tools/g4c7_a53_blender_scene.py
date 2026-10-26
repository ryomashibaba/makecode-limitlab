#!/usr/bin/env python3
"""A53 Blender-native editable studio. This source is NOT an S1/G1 art pass.

Pure Python: python tools/g4c7_a53_blender_scene.py --preflight
In Blender: blender -b --factory-startup --python tools/g4c7_a53_blender_scene.py -- --build --render
Blender writes only NEW assets; cannot overwrite the historical evidence.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "artifacts/g4c7-a53-editable-studio/scene_plan.json"
OUT = ROOT / "artifacts/g4c7-a53-editable-studio/blender-output"

def area(points):
    return sum(a[0]*b[1]-b[0]*a[1] for a,b in
               zip(points,points[1:]+points[:1]))/2

def validate(plan):
    errors = []
    if plan.get("stage") != "A53" or plan.get("version") != 1:
        errors.append("unknown plan version")
    for side in ("west","east"):
        ss=plan.get("banks",{}).get(side,[])
        if len(ss)<4: errors.append(side+": insufficient stations")
        for i,s in enumerate(ss):
            if i and s["y"]<=ss[i-1]["y"]: errors.append(side+": station order")
            if not s["crown"]>s["terrace"]>s["floor"]: errors.append(side+": vertical section")
            if side=="west" and s["inner"]<=s["outer"]: errors.append("west orientation")
            if side=="east" and s["inner"]>=s["outer"]: errors.append("east orientation")
    rooms=plan.get("programRooms",[])
    if {r["id"] for r in rooms}!={"market","culture","research","housing"} or len(rooms)!=4:
        errors.append("program uniqueness")
    for r in rooms:
        if len(r["outline"])<3 or abs(area(r["outline"]))<50: errors.append("room polygon "+r["id"])
        if not r["volumeHeight"]>r["thickness"]>0: errors.append("room height "+r["id"])
    cameras=[c["id"] for c in plan.get("cameraContract",[])]
    if len(cameras)!=9 or len(set(cameras))!=9: errors.append("camera contract")
    if plan["safety"]["construction"]!="FORBIDDEN": errors.append("construction safeguard")
    if len(plan["paths"]["publicArrival"])<4: errors.append("arrival path")
    if errors: raise ValueError("A53 preflight FAILED: "+"; ".join(errors))
    return {"stage":"A53","status":"PLAN PREFLIGHT PASS, NO RENDER",
            "stations":sum(len(s) for s in plan["banks"].values()),
            "programs":len(rooms),"cameras":len(cameras),
            "s1":"NOT RUN","g1":"NOT RUN","g2":"NOT RUN","g3":"NOT RUN","art":"HOLD"}

def build(plan, do_render):
    import bpy
    from mathutils import Vector
    output=OUT/"a53_civic_strata_editable.blend"
    files=[output]
    if do_render: files += [OUT/("render_"+c["id"]+".png") for c in plan["cameraContract"]]
    if any(x.exists() for x in files): raise FileExistsError("Refusing A53 evidence overwrite")
    OUT.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.render.engine="CYCLES"
    scene.cycles.samples=plan["render"]["samples"]
    scene.render.resolution_x,scene.render.resolution_y=plan["render"]["resolution"]
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    def collection(n):
        c=bpy.data.collections.new(n);scene.collection.children.link(c);return c
    architecture=collection("01_ART_EDITABLE_SURFACES")
    programs=collection("02_PROGRAM_SPACES_AND_PATHS")
    context=collection("03_SITE_NOT_FOR_CONSTRUCTION")
    studio=collection("04_LIGHTS_AND_CAMERAS")
    def material(name,color,metal=0,rough=.55,alpha=1):
        m=bpy.data.materials.new(name);m.use_nodes=True
        p=m.node_tree.nodes.get("Principled BSDF")
        p.inputs["Base Color"].default_value=(*color,alpha)
        p.inputs["Metallic"].default_value=metal
        p.inputs["Roughness"].default_value=rough
        if alpha<1:
            p.inputs["Alpha"].default_value=alpha
            if hasattr(m,"surface_render_method"):m.surface_render_method="DITHERED"
        return m
    mats={
        "stone":material("Ivory inhabited ceramic",(.73,.77,.70),.1),
        "shadow":material("Deep recessed mineral",(.11,.17,.20),.22),
        "bronze":material("Cultural bronze",(.45,.27,.15),.63,.37),
        "teal":material("Research translucent blue",(.18,.49,.55),.25,.24,.86),
        "timber":material("Public market timber",(.64,.36,.17),.02),
        "route":material("Warm public stone",(.79,.67,.48),.06,.6)
    }
    def surface(name,vertices,faces,kind,col,thickness=0):
        data=bpy.data.meshes.new(name+"__mesh")
        data.from_pydata(vertices,[],faces);data.update()
        o=bpy.data.objects.new(name,data);col.objects.link(o)
        o.data.materials.append(mats[kind])
        if thickness:
            mod=o.modifiers.new("EDITABLE_SURFACE_DEPTH","SOLIDIFY")
            mod.thickness=thickness
        return o
    # Key artistic change: author 12 section profiles, separate editable skins,
    # no additive array of cubes and no continuous blank outer canopy over programs.
    for side,stations in plan["banks"].items():
        toward=1 if side=="west" else -1
        def profile(s):
            x=s["inner"]
            return [(s["outer"],s["y"],s["floor"]),
                    (x,s["y"],s["floor"]+.7),
                    (x,s["y"],s["terrace"]),
                    (x+6*toward,s["y"],s["terrace"]+5),
                    (x+14*toward,s["y"],s["crown"]-7),
                    (s["outer"],s["y"],s["crown"])]
        rows=[profile(s) for s in stations]
        strips=[("occupied_ground",0,"route",1.5),
                ("court_terrace",2,"stone",1.2),
                ("room_clerestory",3,"teal",1.0),
                ("crown_skyline",4,"stone",1.7),
                ("outer_back",5,"shadow",2.3)]
        for label,edge,kind,thickness in strips:
            v=[rows[i][j] for i in range(len(rows)) for j in (edge,(edge+1)%6)]
            faces=[(i*2,i*2+1,i*2+3,i*2+2) for i in range(len(rows)-1)]
            surface(side.upper()+"__"+label,v,faces,kind,architecture,thickness)
    # Named native meshes remain fully editable; horizontal plan and elevated
    # volume datum are explicitly NOT proof of an actual usable enclosed room.
    for r in plan["programRooms"]:
        verts=[(x,y,r["z"]) for x,y in r["outline"]]
        faces=[tuple(range(len(verts)))]
        surface("EDIT_ROOM_FLOOR__"+r["id"].upper(),verts,faces,
                r["color"],programs,r["thickness"])
        roof=[(x,y,r["z"]+r["volumeHeight"]) for x,y in r["outline"]]
        surface("UNBUILT_HEIGHT_DATUM__"+r["id"].upper(),roof,faces,
                "teal",programs)
    def bezier(name,coords,kind,radius,col):
        data=bpy.data.curves.new(name,"CURVE")
        data.dimensions="3D";data.resolution_u=20
        data.bevel_depth=radius;data.bevel_resolution=3
        s=data.splines.new("BEZIER");s.bezier_points.add(len(coords)-1)
        for q,pt in zip(s.bezier_points,coords):
            q.co=pt;q.handle_left_type="AUTO";q.handle_right_type="AUTO"
        ob=bpy.data.objects.new(name,data);col.objects.link(ob)
        ob.data.materials.append(mats[kind]);return ob
    bezier("PUBLIC_ARRIVAL__EDIT_SPLINE",plan["paths"]["publicArrival"],"route",1.2,programs)
    bezier("SKYLINE_PUBLIC_WALK__EDIT_SPLINE",plan["paths"]["civicSkywalk"],"bronze",1.1,architecture)
    surface("SITE_CONTEXT__NOT_WORLD_EXPORT",
            [(-165,-145,-1),(165,-145,-1),(165,145,-1),(-165,145,-1)],
            [(0,1,2,3)],"stone",context)
    cams={}
    for c in plan["cameraContract"]:
        data=bpy.data.cameras.new(c["id"]);data.lens=c["lens"]
        obj=bpy.data.objects.new("VIEW__"+c["id"],data)
        studio.objects.link(obj);obj.location=c["location"]
        aim=Vector(c["target"])-obj.location
        obj.rotation_euler=aim.to_track_quat("-Z","Y").to_euler()
        cams[c["id"]]=obj
    light_specs=[((-110,-100,200),0,120),((110,10,195),1,95),((0,130,160),2,115)]
    for n,(loc,idx,size) in enumerate(light_specs):
        data=bpy.data.lights.new("StudioArea","AREA")
        data.energy=plan["render"]["lightEnergy"][idx]
        data.shape="DISK";data.size=size
        obj=bpy.data.objects.new("ART_STUDIO_LIGHT_"+str(n),data)
        studio.objects.link(obj);obj.location=loc
        obj.rotation_euler=(Vector((0,0,35))-obj.location).to_track_quat("-Z","Y").to_euler()
    world=bpy.data.worlds.new("Civic overcast sky")
    world.use_nodes=True
    bg=world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value=(.63,.71,.76,1)
    bg.inputs["Strength"].default_value=plan["render"]["worldStrength"]
    scene.world=world;scene.camera=cams["oblique"]
    scene.render.filepath=str(OUT/"render_oblique.png")
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    if do_render:
        for key,cam in cams.items():
            target=OUT/("render_"+key+".png")
            if target.exists():raise FileExistsError("Protected render "+str(target))
            scene.camera=cam;scene.render.filepath=str(target)
            bpy.ops.render.render(write_still=True)
    return {"blend":str(output),"renderCount":len(cams) if do_render else 0,
            "art":"UNASSESSED","G2_G3":"NOT RUN"}

def main():
    import sys
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    parser=argparse.ArgumentParser()
    parser.add_argument("--preflight",action="store_true")
    parser.add_argument("--build",action="store_true")
    parser.add_argument("--render",action="store_true")
    a=parser.parse_args(argv)
    plan=json.loads(PLAN.read_text(encoding="utf-8"))
    print(json.dumps(validate(plan),ensure_ascii=False,indent=2))
    if a.render and not a.build:parser.error("--render requires --build")
    if a.build:print(json.dumps(build(plan,a.render),ensure_ascii=False,indent=2))
    elif not a.preflight:parser.error("Choose --preflight or --build")
if __name__=="__main__":
    main()
