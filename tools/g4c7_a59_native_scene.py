#!/usr/bin/env python3
"""A59 ART-FALSIFICATION. Genuine Blender/Cycles, only two views; NOT an art pass.

The three lower rooms have true solid walls and openings. Upper volumes
are explicitly massing hypotheses, NOT certified apartments or walkable city.
No historical A53 geometry or evidence is touched.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PLAN=ROOT/"artifacts/g4c7-a59-native-two-view/scene_plan.json"
OUT=ROOT/"artifacts/g4c7-a59-native-two-view/native-output"

def validate(p):
    problems=[]
    if p.get("stage")!="A59" or p.get("version")!=1:problems.append("invalid_version")
    if p.get("minecraft")!="FORBIDDEN" or p.get("integration")!="FORBIDDEN":problems.append("construction_not_locked")
    if p.get("safety")!="G2_G3_NOT_RUN":problems.append("fake_safety")
    if set(p.get("cameras",{}))!={"public_heart","oblique"}:problems.append("two_cameras_required")
    if p.get("render",{}).get("engine")!="CYCLES":problems.append("real_cycles_required")
    rooms=p.get("rooms",[])
    if len(rooms)!=3 or {r["id"] for r in rooms}!={"market","maker_culture","research_learning"}:
        problems.append("three_real_rooms_required")
    for r in rooms:
        if r["depth"]<20 or r["width"]<9 or r["door_width"]<3.8 or r["door_width"]>r["width"]-2:
            problems.append("room_geometry_"+r["id"])
        if r["z"]!=0:problems.append("room_floor_"+r["id"])
    blocks=p.get("upper_mass_studies",[])
    if len(blocks)!=9 or len({b["id"] for b in blocks})!=9:problems.append("nine_masses")
    for b in blocks:
        if b["top"]<=b["bottom"]+12 or b["bottom"]<5:problems.append("unusable_mass_"+b["id"])
        if b["x1"]-b["x0"]<15 or b["depth"]<20:problems.append("invalid_footprint_"+b["id"])
    if problems:raise ValueError("A59_G0_PLAN_REJECT "+",".join(problems))
    return {"preflight":"PASS","rooms":3,"massing_hypotheses":9,
            "native_3d":"NOT_RUN","S1":"NOT_RUN","G1":"NOT_RUN",
            "G2":"NOT_RUN","G3":"NOT_RUN","art":"HOLD"}

def negative(p):
    tests=[
     ("unlock_construction",lambda x:x.__setitem__("minecraft","ALLOWED")),
     ("remove_camera",lambda x:x["cameras"].pop("oblique")),
     ("shallow_room",lambda x:x["rooms"][0].__setitem__("depth",2)),
     ("fake_opening",lambda x:x["rooms"][0].__setitem__("door_width",15)),
     ("fake_safety",lambda x:x.__setitem__("safety","G3_PASS")),
     ("unsupported_mass",lambda x:x["upper_mass_studies"][0].__setitem__("bottom",-5))]
    for name,f in tests:
        bad=copy.deepcopy(p);f(bad)
        try:validate(bad)
        except ValueError:print("DETECTED",name)
        else:raise AssertionError("Negative control escaped: "+name)
    print("A59_NEGATIVE_CONTROLS_6_OF_6_PASS")

def build(p):
    import bpy
    from mathutils import Vector
    native=OUT/"a59_occupied_city_slice.blend"
    images={k:OUT/("render_"+k+".png") for k in p["cameras"]}
    if any(t.exists() for t in [native,*images.values()]):
        raise FileExistsError("Never overwrite original A59 files")
    OUT.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
    sc=bpy.context.scene
    sc.render.engine="CYCLES";sc.cycles.samples=24
    sc.cycles.use_denoising=True
    sc.render.resolution_x,sc.render.resolution_y=[960,720]
    sc.render.resolution_percentage=100
    sc.render.image_settings.file_format="PNG"
    sc.view_settings.view_transform="AgX"
    def group(n):
        a=bpy.data.collections.new(n);sc.collection.children.link(a);return a
    rooms=group("01_TRUE_ROOM_MESHES_AND_PHYSICAL_DOORS")
    program=group("02_REAL_FURNISHINGS")
    city=group("03_UPPER_MASSES_ONLY_NOT_INHABITABILITY_PROOF")
    facade=group("04_ACTIVITY_EDGES_AND_GARDEN_HINTS")
    rig=group("05_SUN_CAMERA_CONTEXT")
    def material(n,c,metal=.1,rough=.45,emit=0):
        m=bpy.data.materials.new(n);m.use_nodes=True
        s=m.node_tree.nodes.get("Principled BSDF")
        s.inputs["Base Color"].default_value=(*c,1)
        s.inputs["Metallic"].default_value=metal
        s.inputs["Roughness"].default_value=rough
        if emit:
            s.inputs["Emission Color"].default_value=(*c,1)
            s.inputs["Emission Strength"].default_value=emit
        return m
    mats={
    "bone":material("Pale blue brushed ceramic",(.51,.70,.75),.35,.3),
    "dark":material("Dark cyan load core",(.034,.10,.18),.49,.39),
    "glass":material("Pearl active glazing",(.54,.85,.86),.18,.25,.24),
    "warm":material("Public room warm interior",(.85,.67,.37),.10,.63,.12),
    "copper":material("Activity brass",(.7,.39,.19),.58,.30),
    "road":material("Composite civic pedestrian road",(.37,.48,.56),.08,.64),
    "plant":material("Terrace canopy foliage",(.10,.35,.30),0,.63),
    "trim":material("Titanium edged facade",(.73,.77,.80),.6,.28)
    }
    def cube(n,xyz,scale,mat,col,b=.06):
        bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
        ob=bpy.context.object;ob.name=n
        for c in list(ob.users_collection):c.objects.unlink(ob)
        col.objects.link(ob);ob.dimensions=scale
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        ob.data.materials.append(mats[mat])
        if b:
            mod=ob.modifiers.new("Independent_editable_edge","BEVEL")
            mod.width=b;mod.segments=2
        return ob
    def form(n,poly,z0,z1,mat,col):
        l=len(poly)
        v=[(x,y,z0) for x,y in poly]+[(x,y,z1) for x,y in poly]
        f=[tuple(reversed(range(l))),tuple(range(l,2*l))]
        f += [(i,(i+1)%l,(i+1)%l+l,i+l) for i in range(l)]
        mesh=bpy.data.meshes.new(n+"_mesh");mesh.from_pydata(v,[],f);mesh.update()
        ob=bpy.data.objects.new(n,mesh);col.objects.link(ob);ob.data.materials.append(mats[mat])
        bev=ob.modifiers.new("Authored_architectural_corner","BEVEL")
        bev.width=.42;bev.segments=2
        return ob
    # All S1 geometry shares top level z=0, including actual solid room floors.
    cube("PUBLIC_HEART_ACTUAL_FLOOR",(0,12,-.65),(47,58,1.3),"road",rooms,.5)
    cube("RECESSED_PUBLIC_STREET",(0,6,.055),(11,29,.11),"trim",rooms,.02)
    for r in p["rooms"]:
        n=r["id"];x=r["x"];y=r["front_y"];w=r["width"];d=r["depth"];a=r["door_width"]
        def B(s,loc,dim,mat="bone"):
            return cube(n+"_"+s,loc,dim,mat,rooms,.05)
        B("actual_floor",(x,y+d/2,-.55),(w,d,1.1),"road")
        B("back_wall",(x,y+d-.3,2.8),(w,.6,5.6),"dark")
        B("side_L",(x-w/2+.24,y+d/2,2.8),(.48,d,5.6))
        B("side_R",(x+w/2-.24,y+d/2,2.8),(.48,d,5.6))
        side=(w-a)/2
        B("front_pier_L",(x-(w+a)/4,y+.24,2.0),(side,.48,4))
        B("front_pier_R",(x+(w+a)/4,y+.24,2.0),(side,.48,4))
        B("front_lintel",(x,y+.24,5.0),(a,.48,1.2),"trim")
        # True aperture without a wall mesh inside; roof cut creates real sky access.
        B("open_roof_left",(x-w*.325,y+d*.6,6.0),(w*.32,d*.75,.5),"dark")
        B("open_roof_right",(x+w*.325,y+d*.6,6.0),(w*.32,d*.75,.5),"dark")
        B("roof_rear",(x,y+d*.94,6.0),(w,d*.12,.5),"dark")
        cube(n+"_real_aperture_sill",(x,y-.25,.20),(a,.3,.4),"trim",facade,.04)
        if n=="market":
            for j,yy in enumerate((y+7,y+12,y+17)):
                for i,xx in enumerate((x-2.0,x+2.0)):
                    cube(f"MARKET_COUNTER_{i}_{j}",(xx,yy,.76),(1.55,2.4,1.52),"copper",program,.13)
                    cube(f"MARKET_GOODS_{i}_{j}",(xx,yy,1.58),(1.3,1.25,.18),"warm",program,.04)
        elif n=="maker_culture":
            for j,yy in enumerate((y+6,y+11,y+16)):
                cube(f"MAKER_WORKBENCH_{j}",(x,yy,.78),(3.2,1.9,1.56),"copper",program,.09)
                cube(f"MAKER_SCULPTURE_{j}",(x-1,yy,1.85),(.6,.45,.62),"glass",program,.09)
        else:
            for j,yy in enumerate((y+6,y+12,y+17)):
                cube(f"LEARNING_DESK_{j}",(x,yy,.75),(3.1,1.7,1.5),"warm",program,.10)
                for i,xx in enumerate((x-2.3,x+2.3)):
                    cube(f"LEARNING_BOOKSHELF_{i}_{j}",(xx,yy,1.65),(.55,2.2,3.3),"copper",program,.03)
    # Nine DIFFERENT manually laid-out positive masses, not A53 long ribbon,
    # not approved real rooms. This must survive the distant art image on its own.
    for u in p["upper_mass_studies"]:
        x0,x1,y,depth=u["x0"],u["x1"],u["front_y"],u["depth"]
        outline=[(x0,y+6),(x0+5,y-2),(x1-6,y),(x1,y+9),
                 (x1-3,y+depth),(x0+8,y+depth+3)]
        form(u["id"]+"_STUDY_NOT_CERTIFIED_ROOM",outline,u["bottom"],u["top"],u["mat"],city)
        levels=u["levels"]
        for k,z in enumerate(levels):
            # Occupied facade is a hypothesis of density, not wall/window connectivity QA
            span=x1-x0
            for i in range(int(span//5)):
                cx=x0+(i+.52)*5
                if (k+i)%6==2:continue
                cube(u["id"]+f"_FACADE_WINDOW_{k}_{i}",(cx,y-2.19,z),
                     (2.8,.35,2.7),"glass" if i%3 else "warm",facade,.06)
            cube(u["id"]+f"_OCCUPANCY_CORNICE_{k}",((x0+x1)/2,y-2.7,z-2),
                 (.94*span,1.35,.7),"trim",facade,.12)
    # Thick, positive volumes at the program transitions: not thin skybridges.
    form("CIVIC_SEAM_WEST_MASSING_ONLY",
         [(-47,44),(-12,44),(-10,57),(-24,68),(-48,65)],25,41,"dark",city)
    form("CIVIC_SEAM_EAST_MASSING_ONLY",
         [(-1,48),(42,44),(43,63),(28,74),(-1,66)],30,45,"bone",city)
    cube("NEUTRAL_SITE_NOT_MINECRAFT_WORLD",(0,55,-3),(235,180,4),"road",rig,0)
    sun=bpy.data.lights.new("REAL_WORLD_DIRECTIONAL_DAYLIGHT","SUN");sun.energy=2.2
    solar=bpy.data.objects.new("REAL_WORLD_DIRECTIONAL_DAYLIGHT",sun)
    rig.objects.link(solar);solar.rotation_euler=(.45,-.6,-.4)
    for n,loc,en,size in (("AREA_PUBLIC",(0,-38,30),7500,34),
                          ("AREA_CITY",(-105,-80,140),25000,96)):
        d=bpy.data.lights.new(n,"AREA");d.energy=en;d.shape="DISK";d.size=size
        o=bpy.data.objects.new(n,d);rig.objects.link(o);o.location=loc
        o.rotation_euler=(Vector((0,25,27))-o.location).to_track_quat("-Z","Y").to_euler()
    world=bpy.data.worlds.new("Daylight atmosphere")
    world.use_nodes=True
    bg=world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value=(.33,.54,.68,1)
    bg.inputs["Strength"].default_value=.7
    sc.world=world
    cams={}
    for name,c in p["cameras"].items():
        d=bpy.data.cameras.new(name);d.angle=math.radians(c["horizontal_fov_degrees"])
        o=bpy.data.objects.new("VIEW_"+name,d);rig.objects.link(o)
        o.location=c["position"]
        o.rotation_euler=(Vector(c["target"])-o.location).to_track_quat("-Z","Y").to_euler()
        cams[name]=o
    dg=bpy.context.evaluated_depsgraph_get()
    eye=cams["public_heart"].location
    assert math.isclose(eye.z,1.7,abs_tol=.000001)
    hit,point,nrm,idx,obj,matx=sc.ray_cast(dg,eye,Vector((0,0,-1)),distance=4)
    assert hit and abs(point.z)<.06 and obj.name=="PUBLIC_HEART_ACTUAL_FLOOR",repr((hit,tuple(point),obj.name if obj else None))
    for r in p["rooms"]:
        target=Vector((r["x"],r["front_y"]+3,1.7)); direction=target-eye
        hit,point,nrm,idx,obj,matx=sc.ray_cast(dg,eye,direction.normalized(),distance=direction.length)
        print("TRUE_3D_APERTURE_RAY",r["id"],"BLOCKED_"+obj.name if hit else "CLEAR")
    sc.camera=cams["oblique"]
    bpy.ops.wm.save_as_mainfile(filepath=str(native))
    for name,o in cams.items():
        sc.camera=o;sc.render.filepath=str(images[name])
        bpy.ops.render.render(write_still=True)
    return {"blender":str(native),"images":list(images),"S1_ART":"NOT_ASSESSED","G1":"NOT_RUN",
            "G2":"NOT_RUN","G3":"NOT_RUN","overall":"ART_HOLD"}

def main():
    import sys
    argv=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else sys.argv[1:]
    a=argparse.ArgumentParser()
    a.add_argument("--preflight",action="store_true")
    a.add_argument("--negatives",action="store_true")
    a.add_argument("--build-render",action="store_true")
    v=a.parse_args(argv)
    p=json.loads(PLAN.read_text(encoding="utf-8"))
    print(json.dumps(validate(p),indent=2))
    if v.negatives:negative(p)
    if v.build_render:print(json.dumps(build(p),indent=2))
    if not any((v.preflight,v.negatives,v.build_render)):a.error("no action")
if __name__=="__main__":main()
