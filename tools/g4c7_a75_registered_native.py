#!/usr/bin/env python3
"""A75: A73's single geometry datum -> EDITABLE Blender civic section + genuine Cycles views.

This is a visual FALSIFICATION of a still-unsatisfactory future-city design, NOT an
architectural, structural, collision, habitation, artistic or Minecraft approval.
Preserves every A73/A74 file and never overwrites A75 output.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, struct, zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts/g4c7-a75-registered-native/native-output"
SOURCE=ROOT/"tools/g4c7_a73_topology_fabric.py"
A75_STAGE="A75"
PROGRAMS={"MARKET":{"floor_color":"copper","level":0.0,"use":"market counter and exchange"},
          "MAKER":{"floor_color":"blue","level":0.0,"use":"workshop tools and fabrication"},
          "READING":{"floor_color":"gold","level":7.2,"use":"research reading"},
          "HOUSING":{"floor_color":"clay","level":12.6,"use":"domestic living"}}
FORMAL={n:"NOT_RUN" for n in ("S1","G1","G2","G3")}
def upstream():
    spec=importlib.util.spec_from_file_location("g4c7_a73_source", SOURCE)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
def invariant():
    a=upstream(); p=a.make_plan()
    assert set(p["rooms"])==set(PROGRAMS)
    assert a.CONTRACT["minecraft_construction"]=="FORBIDDEN"
    for name,r in p["rooms"].items():
        assert abs(r["contact"]-r["entrance_width"])<1e-5,(name,r["contact"],r["entrance_width"])
        assert abs(r["z"]-PROGRAMS[name]["level"])<1e-8
    assert len(p["stairs"])==3
    assert sum(t[2] for t in p["stairs"])==70
    assert p["nodes"]["PUBLIC_EYE"]==(0.,-16.,0.)
    return a,p
def image_integrity(filename):
    buf=Path(filename).read_bytes()
    assert buf[:8]==b"\x89PNG\r\n\x1a\n"
    idx=8;seen=[]
    while idx<len(buf):
        n=struct.unpack_from(">I",buf,idx)[0];kind=buf[idx+4:idx+8]
        payload=buf[idx+8:idx+8+n]
        crc=struct.unpack_from(">I",buf,idx+8+n)[0]
        assert zlib.crc32(kind+payload)&0xffffffff==crc
        if kind==b"IHDR":assert struct.unpack(">II",payload[:8])==(960,720)
        idx+=n+12;seen.append(kind)
        if kind==b"IEND":break
    assert idx==len(buf) and b"IDAT" in seen and seen[-1]==b"IEND"
    return {"sha256":hashlib.sha256(buf).hexdigest(),"bytes":len(buf)}
def build():
    import bpy
    from mathutils import Vector
    from shapely.ops import triangulate
    _,plan=invariant()
    OUT.mkdir(parents=True,exist_ok=True)
    targets=[OUT/"a75_registered_civic_section.blend", OUT/"public_eye.png",
             OUT/"oblique.png",OUT/"a75_manifest.json"]
    if any(f.exists() for f in targets):raise FileExistsError("A75 append-only protection")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    scene=bpy.context.scene
    scene.render.engine="CYCLES";scene.cycles.samples=16
    scene.render.resolution_x=960;scene.render.resolution_y=720
    scene.render.resolution_percentage=100
    scene.render.image_settings.file_format="PNG"
    scene.view_settings.view_transform="AgX"
    collections={}
    for group in ("01_A73_PUBLIC_FLOORS","02_A73_ACTUAL_ROOM_FLOORS",
                  "03_4_INHABITED_FOLDED_ENVELOPES","04_A73_70_STAIR_TREADS",
                  "05_INSIDE_PROGRAM_ACTIVITY","06_LIGHTS_AND_TWO_CAMERAS"):
        ob=bpy.data.collections.new(group);scene.collection.children.link(ob);collections[group]=ob
    def material(name,rgb,metal=0.0,emission=0.0):
        mat=bpy.data.materials.new(name);mat.use_nodes=True
        p=mat.node_tree.nodes.get("Principled BSDF")
        p.inputs["Base Color"].default_value=(*rgb,1)
        p.inputs["Metallic"].default_value=metal
        p.inputs["Roughness"].default_value=.47
        if emission:
            p.inputs["Emission Color"].default_value=(*rgb,1)
            p.inputs["Emission Strength"].default_value=emission
        return mat
    mats={
       "ground":material("Warm civic travertine",(.42,.48,.48)),
       "mineral":material("Weathered structural mineral",(.24,.36,.41),.20),
       "shadow":material("Dark occupied panel joints",(.065,.12,.17),.35),
       "copper":material("Market copper interior",(.69,.38,.21),.23),
       "blue":material("Maker blue glass and ceramic",(.14,.57,.60),.25),
       "gold":material("Reading amber ceramic",(.83,.64,.32),.12),
       "clay":material("Housing red ochre",(.59,.40,.35),.12),
       "plants":material("Plant canopy",(.13,.36,.27)),
       "light":material("Small human scale lamp",(.94,.69,.35),0,.15)
    }
    def mesh(name,verts,faces,mat,collection,thickness=0):
        data=bpy.data.meshes.new(name+"_MESH")
        data.from_pydata(verts,[],faces);data.update()
        ob=bpy.data.objects.new(name,data);collections[collection].objects.link(ob)
        data.materials.append(mats[mat])
        if thickness:
            mod=ob.modifiers.new("Editable_surface_thickness","SOLIDIFY")
            mod.thickness=thickness
        return ob
    def face(name,p,kind,group,thickness=0):
        return mesh(name,p,[tuple(range(len(p)))],kind,group,thickness)
    def cube(name,xyz,dims,kind,group,rotation=0):
        bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
        o=bpy.context.object;o.name=name;o.dimensions=dims
        bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        o.rotation_euler.z=rotation
        for collection in list(o.users_collection):collection.objects.unlink(o)
        collections[group].objects.link(o);o.data.materials.append(mats[kind]);return o
    def floor_poly(name,poly,z,kind,group):
        parts=([poly] if poly.geom_type=="Polygon" else list(poly.geoms))
        count=0
        for k,part in enumerate(parts):
            for j,tri in enumerate(triangulate(part)):
                # A73 uses the same triangulation rule; never fill voids across concave boundaries
                if part.covers(tri.representative_point()):
                    xyz=[(pt[0],pt[1],z) for pt in list(tri.exterior.coords)[:3]]
                    mesh(name+"_"+str(k)+"_"+str(j),xyz,[(0,1,2)],kind,group,.28)
                    count+=1
        return count
    metrics={"public_floor_faces":0,"rooms":{},"stairs":0,"real_views":2}
    for z,polygon in plan["floors"].items():
        metrics["public_floor_faces"]+=floor_poly("A73_SHARED_CIVIC_SURFACE_Z"+str(z),polygon,z,
            "ground","01_A73_PUBLIC_FLOORS")
    for name,r in plan["rooms"].items():
        program=PROGRAMS[name];z=r["z"]
        metrics["rooms"][name]={"z":z,"open_width":round(r["entrance_width"],3),
                                "contact":round(r["contact"],3),"geometry":"actual_floor_and_open_front"}
        floor_poly(name+"_INTERIOR_3D_FLOOR",r["polygon"],z,program["floor_color"],
                   "02_A73_ACTUAL_ROOM_FLOORS")
        coords=list(r["polygon"].exterior.coords)[:-1]
        # Front geometry is derived EXACTLY from A73 room's opening, not A72's independent polygon.
        a,b=coords[0],coords[1];L,R=list(r["door"].coords)
        def wall_segment(label,p0,p1,top,left_top=None):
            hi0=top if left_top is None else left_top
            face(name+"_"+label,[(p0[0],p0[1],z),(p1[0],p1[1],z),
                 (p1[0],p1[1],z+top),(p0[0],p0[1],z+hi0)],
                 "mineral","03_4_INHABITED_FOLDED_ENVELOPES",.44)
        # Opening is REAL, and the room/route ends share their georeferenced source.
        line_order=[a,L,R,b]
        for i,(p0,p1) in enumerate(((a,L),(R,b))):
            wall_segment("ACTUAL_FRONT_WALL_"+str(i),p0,p1,6.6)
        face(name+"_BEAM_ABOVE_ACTUAL_OPENING",
             [(L[0],L[1],z+4.5),(R[0],R[1],z+4.5),
              (R[0],R[1],z+6.8),(L[0],L[1],z+6.8)],
             program["floor_color"],"03_4_INHABITED_FOLDED_ENVELOPES",.48)
        # Five non-identical steep folds per space; top offsets authored per use.
        height={"MARKET":[6.8,9.4,7.2,8.2],
                "MAKER":[7.7,10.6,9.8,7.4],
                "READING":[7.6,10.8,8.1,8.8],
                "HOUSING":[6.8,9.1,7.4,8.5]}[name]
        for idx in range(1,len(coords)):
            u,v=coords[idx],coords[(idx+1)%len(coords)]
            h0=height[idx%4];h1=height[(idx+1)%4]
            face(name+"_DIFFERENTIATED_OCCUPIED_SIDE_"+str(idx),
                 [(u[0],u[1],z),(v[0],v[1],z),
                  (v[0],v[1],z+h1),(u[0],u[1],z+h0)],
                 "mineral" if idx%2 else "shadow","03_4_INHABITED_FOLDED_ENVELOPES",.50)
        # Roof and outer form wrap ACTUAL room only, no ring / bridge / false central monument.
        p0,p1,p2,p3=coords[:4]
        face(name+"_ASYMMETRIC_INHABITED_COVER",
             [(p0[0],p0[1],z+6.8),(p1[0],p1[1],z+7.0),
              (p2[0],p2[1],z+10.2),(p3[0],p3[1],z+9.2)],
             program["floor_color"],"03_4_INHABITED_FOLDED_ENVELOPES",.35)
        c=r["polygon"].representative_point()
        # Identifiable real furnishings are placed inside representative interior floor polygon.
        for i in range(3):
            fx=c.x+(i-1)*1.45;fy=c.y+(i%2-.5)*1.6
            cube(name+"_REAL_WORK_OR_LIVING_STATION_"+str(i),(fx,fy,z+.65),
                 (1.5,.85,1.3),program["floor_color"],"05_INSIDE_PROGRAM_ACTIVITY")
            cube(name+"_REAL_LAMP_"+str(i),(fx,fy,z+1.65),
                 (.25,.25,.25),"light","05_INSIDE_PROGRAM_ACTIVITY")
    for key_a,key_b,steps,A,B in plan["stairs"]:
        dx=(B[0]-A[0])/steps;dy=(B[1]-A[1])/steps
        yaw=math.atan2(dy,dx)
        for i in range(steps):
            cx=A[0]+(i+.5)*dx;cy=A[1]+(i+.5)*dy
            top=A[2]+(i+1)*.18
            cube(key_a+"_TO_"+key_b+"_REAL_TREAD_"+str(i),
                (cx,cy,top-.11),(.32,3.7,.22),"ground",
                "04_A73_70_STAIR_TREADS",yaw)
        metrics["stairs"]+=steps
    # Human scale elements at ACTUAL graph nodes; no additional scenic bridges/rings.
    for j,key in enumerate(["CIVIC_HEART","MID_CIVIC","READING_ENTRY","GARDEN"]):
        x,y,z=plan["nodes"][key]
        cube("LIVING_SITE_PLANTER_"+key,(x+3.8,y+3,z+.42),(1.6,1.6,.84),
             "copper","05_INSIDE_PROGRAM_ACTIVITY")
        cube("LEAF_CANOPY_"+key,(x+3.8,y+3,z+2.6),(2.2,2.3,2.4),
             "plants","05_INSIDE_PROGRAM_ACTIVITY")
    cube("NOT_G2_TERRAIN_CONTEXT",(9,24,-2.7),(135,145,3),
         "shadow","06_LIGHTS_AND_TWO_CAMERAS")
    world=bpy.data.worlds.new("G0 clear cool daytime")
    world.use_nodes=True;world.node_tree.nodes.get("Background").inputs["Strength"].default_value=.75
    world.node_tree.nodes.get("Background").inputs["Color"].default_value=(.48,.63,.70,1)
    scene.world=world
    sun=bpy.data.lights.new("Exterior sun","SUN");sun.energy=2.5
    obj=bpy.data.objects.new("G0 sunshine",sun);collections["06_LIGHTS_AND_TWO_CAMERAS"].objects.link(obj)
    obj.rotation_euler=(.55,-.45,.40)
    for name,pos,power,size in [("front",(0,-42,38),4400,28),
                                 ("back",(75,80,100),7600,58)]:
        light=bpy.data.lights.new(name,"AREA");light.energy=power
        light.shape="DISK";light.size=size
        ob=bpy.data.objects.new("G0_AREA_"+name,light)
        collections["06_LIGHTS_AND_TWO_CAMERAS"].objects.link(ob);ob.location=pos
        ob.rotation_euler=(Vector((0,18,7))-ob.location).to_track_quat("-Z","Y").to_euler()
    eyes={"public_eye":(0,-16,1.7),"oblique":(96,-103,90)}
    looks={"public_eye":(0,7,3),"oblique":(12,22,10)}
    cameras={}
    for name,pos in eyes.items():
        d=bpy.data.cameras.new("ACTUAL_VIEW_"+name);d.lens=27 if name=="public_eye" else 37
        cam=bpy.data.objects.new("G0_CAMERA_"+name,d)
        collections["06_LIGHTS_AND_TWO_CAMERAS"].objects.link(cam);cam.location=pos
        cam.rotation_euler=(Vector(looks[name])-cam.location).to_track_quat("-Z","Y").to_euler()
        cameras[name]=cam
    scene.camera=cameras["oblique"]
    blend=targets[0]
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    views={}
    for name,cam in cameras.items():
        scene.camera=cam
        filepath=OUT/(name+".png")
        scene.render.filepath=str(filepath)
        bpy.ops.render.render(write_still=True)
        views[name]=image_integrity(filepath)
    assert metrics["stairs"]==70
    manifest={"stage":"A75","renderer":"BLENDER_4_5_CYCLES","art":"NOT_ASSESSED",
         "overall_art":"HOLD","formal":FORMAL,
         "minecraft":"FORBIDDEN","city_integration":"FORBIDDEN",
         "model_kind":"SINGLE_A73_G0_REGISTERED_EDITORIAL_NEIGHBOURHOOD_NOT_KM_CITY",
         "A73_geometry_verified":True,"local_floor_only":True,
         "real_walkability":False,"human_collision":False,"structure_support":False,
         "exact_public_eye":[0,-16,1.7],
         "true_cameras":2,"technical_metrics":metrics,"views":views,
         "blend_sha256":hashlib.sha256(blend.read_bytes()).hexdigest()}
    targets[3].write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
    print("A75_TRUE_EDITABLE_A73_BASED_NATIVE_BLENDER_SAVED__NO_ART_APPROVAL")
def main():
    pa=argparse.ArgumentParser()
    pa.add_argument("--preflight",action="store_true")
    pa.add_argument("--negatives",action="store_true")
    pa.add_argument("--render",action="store_true")
    args=pa.parse_args()
    a,plan=invariant()
    print(json.dumps({"stage":"A75","kind":"G0_SOURCE_ALIGNED_NEEDED_NOT_SUFFICIENT",
        "contacts":{name:{"door":r["entrance_width"],"contact":round(r["contact"],6)}
                    for name,r in plan["rooms"].items()},
        "stair_steps":sum(x[2] for x in plan["stairs"]),
        "formal":FORMAL,"art":"NOT_APPROVED",
        "minecraft":"FORBIDDEN"},indent=2))
    if args.negatives:a.run_negative_controls()
    if args.render:build()
if __name__=="__main__":main()
