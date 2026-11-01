#!/usr/bin/env python3
"""G4-C7 M37-N. Bounded source-mesh SUBTRACTION + controlled transparent
factory gallery in NEW scene only; M37-L/M37-M original source protected.
Not a complete city, not safety/ART PASS, no MakeCode or game writes.
"""
import bpy,hashlib,json,math,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path("artifacts/g4c7-m37m-verified-native-review-workspace-art-hold")
SOURCE=ROOT/"M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD.blend"
OUT=Path("artifacts/g4c7-m37n-shipyard-view-build")
OUT.mkdir(parents=True,exist_ok=True)
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
old=json.loads((ROOT/"M37M_REVIEW_STUDIO_MANIFEST.json").read_text())
assert sha(SOURCE)==old["native_blend"]["sha256"]
assert old["not_proven"]["Minecraft"]=="FORBIDDEN"
bpy.ops.wm.open_mainfile(filepath=str(SOURCE.resolve()))
src=bpy.data.scenes["M37L_SINGLE_CITY_MASTER_AUTHOR_ART_HOLD"]
wrk=bpy.data.scenes["M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD"]
assert len([o for o in src.objects if o.type=="MESH"])==199
assert len([o for o in wrk.objects if o.type=="MESH"])==199
SCENE="M37N_MAKER_PUBLIC_VISTA_DIRECT_AUTHOR_EDIT_ART_HOLD"
new=bpy.data.scenes.new(SCENE)
new.world=wrk.world
for key,value in {
 "M37N_ART":"EARLY_HOLD_UNREVIEWED",
 "M37N_REFERENCE_ART":"M37L_ART_REJECT_UNCHANGED",
 "M37N_FORMAL_331_993":"NOT_RUN",
 "M37N_MINECRAFT":"FORBIDDEN","M37N_USER_ADOPTION":0,
 "M37N_SCALE":"ABSTRACT_RESEARCH_UNITS_NOT_MINECRAFT_BLOCKS",
 "M37N_METHOD":"LOCAL_REAL_SHELL_MESH_SUBTRACTION_AND_SEALED_VIEW_GALLERY",
 "M37N_PARENT_SHA256":sha(SOURCE)}.items():new[key]=value
col=bpy.data.collections.new("M37N_RESEARCH_AUTHOR_REAL_EDIT_ONLY")
new.collection.children.link(col)
map_={}
for o in wrk.objects:
    c=o.copy()
    if o.data:c.data=o.data.copy()
    assert o.name.startswith("M37M_EDIT_"),o.name
    c.name="M37N_"+o.name[len("M37M_EDIT_"):]
    col.objects.link(c);map_[o.name[len("M37M_EDIT_"):]]=c
for o in wrk.objects:
    if o.parent:map_[o.name[len("M37M_EDIT_"):]].parent=map_[o.parent.name[len("M37M_EDIT_"):]]
assert sum(o.type=="MESH" for o in new.objects)==199
assert all(c.data.as_pointer()!=wrk.objects["M37M_EDIT_"+k].data.as_pointer()
           for k,c in map_.items() if c.type=="MESH")
# Preserve original M37-L camera transformations. Additional view cameras are
# separate and never replace/remove an original fixed viewpoint.
for name in ("SOUTH","NORTH","AERIAL","PUBLIC_EYE","MAKER_EYE",
             "RESEARCH_EYE","HABITAT_EYE","UPPER_EYE","SKYLINE_SIDE"):
    assert "M37L_CAMERA_"+name in map_
# Edit the ORIGINAL COPIED SHELL MESH DATABLOCKS themselves. Each old 8-vertex
# cross-section hull bay becomes two shortened anchored bands at t=[0,.12]
# and [.88,1], leaving a real (not painted) 76% central outdoor aperture.
# Only at assembly-related station spans; never repeat across the whole city.
cut_names=["M37L_SHELL_%02d_%02d"%(section,angle)
           for section in (3,4) for angle in (1,2,3,4,5)]
def band_from_native_8(verts,t0,t1):
    assert len(verts)==8
    p=[Vector(x) for x in verts]
    def between(t):return [tuple(p[i].lerp(p[i+4],t)) for i in range(4)]
    v=between(t0)+between(t1)
    faces=[(3,2,1,0),(4,5,6,7)]+[
        (i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]
    return v,faces
cuts={}
for name in cut_names:
    o=map_[name]
    assert o.type=="MESH" and len(o.data.vertices)==8 and len(o.data.polygons)==6,name
    before=[tuple(v.co) for v in o.data.vertices]
    a,fa=band_from_native_8(before,0,.12)
    b,fb=band_from_native_8(before,.88,1)
    newv=a+b
    newf=fa+[tuple(i+8 for i in face) for face in fb]
    o.data.clear_geometry()
    o.data.from_pydata(newv,[],newf)
    o.data.update()
    assert len(o.data.vertices)==16 and len(o.data.polygons)==12
    o["M37N_ROLE"]="EXISTING_REAL_SHELL_DIRECTLY_SPLIT_FOR_PUBLIC_SHIPYARD_OUTLOOK"
    cuts[name]={"before_vertices":8,"after_vertices":16,
                "source_station_fraction_removed":[.12,.88],
                "source_stored_vertices":before}
# Keep a physical manufacturing/public separation in the revised scene.
# Do NOT delete the partition to obtain a misleading clear view.
barrier_name="M37L_MAKER_BOUNDARY_ACTUAL_MEMBRANE"
barrier=map_[barrier_name]
assert barrier.type=="MESH" and len(barrier.data.vertices)==8
viewglass=bpy.data.materials.new("M37N_TRUE_TRANSMISSIVE_VISITOR_SEAL")
viewglass.use_nodes=True
bsdf=viewglass.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value=(.84,.96,.94,1)
bsdf.inputs["Transmission Weight"].default_value=.995
bsdf.inputs["Roughness"].default_value=.02
bsdf.inputs["IOR"].default_value=1.07
barrier.data.materials.clear()
barrier.data.materials.append(viewglass)
barrier["M37N_ROLE"]="SEALED_TRANSMISSIVE_WORKZONE_VIEW_NOT_PHYSICAL_PASSAGE"
# One genuine working frontage gallery FLOOR, located on the public side of the
# intact glass barrier. This is an occupied-use spatial proposition, not
# broad replicating slab city. Its access and structural support are NOT proven.
deckmat=bpy.data.materials.new("M37N_PUBLIC_FACTORY_OBSERVATION_DECK")
deckmat.diffuse_color=(.46,.43,.32,1)
deckmat.use_nodes=True
deckmat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(.46,.43,.32,1)
metal=bpy.data.materials.new("M37N_STRUCTURAL_VISITOR_GUARD")
metal.diffuse_color=(.25,.31,.35,1)
metal.use_nodes=True
metal.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(.25,.31,.35,1)
extra=[]
def create_prism(name,poly,z0,z1,mat,role):
    assert len(poly)==4 and z0<z1
    v=[(x,y,z) for z in (z0,z1) for x,y in poly]
    f=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]
    mesh=bpy.data.meshes.new("M37N_"+name+"_Mesh")
    mesh.from_pydata(v,[],f);mesh.update()
    obj=bpy.data.objects.new("M37N_"+name,mesh)
    col.objects.link(obj);mesh.materials.append(mat)
    obj["M37N_ROLE"]=role;extra.append(obj)
    return obj
create_prism("PUBLIC_MAKER_FRONTAGE_WALKING_FLOOR",
     [(9,-60),(22.8,-60),(22.8,15),(9,15)],19.0,19.8,deckmat,
     "ACTUAL_VISITOR_FLOOR_NOT_CONNECTED_ROUTE_CERTIFIED")
# Vertical guard on LEFT edge and entrance end. The existing sealed glazing
# is right edge; support and escape routes are still UNVERIFIED.
create_prism("PUBLIC_GALLERY_SIDE_GUARD",
     [(8.75,-60),(9.12,-60),(9.12,15),(8.75,15)],19.8,21.65,metal,
     "GUARD_GEOMETRY_NOT_CERTIFIED_TO_METER_STANDARD")
create_prism("PUBLIC_GALLERY_END_GUARD",
     [(9,14.7),(22.8,14.7),(22.8,15),(9,15)],19.8,21.65,metal,
     "GUARD_GEOMETRY_NOT_CERTIFIED")
# Two unequal dedicated cantilever bearings at existing program transitions.
# They are real volumes, but this is not a structural load certification.
create_prism("MAKER_PUBLIC_PIER_A",
     [(10,-42),(21,-42),(21,-39),(10,-39)],14,19.0,metal,
     "BEARING_POSITION_STUDY_NOT_STRUCTURAL_CERTIFIED")
create_prism("MAKER_PUBLIC_PIER_B",
     [(10,-3),(21,-3),(21,1),(10,1)],14,19.0,metal,
     "BEARING_POSITION_STUDY_NOT_STRUCTURAL_CERTIFIED")
from mathutils import Vector
def camera(key,loc,target,lens):
    data=bpy.data.cameras.new("M37N_"+key+"_CameraData")
    ob=bpy.data.objects.new("M37N_CAMERA_"+key,data)
    col.objects.link(ob);ob.location=loc
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
    data.lens=lens
    return ob
camera("VISITOR_GALLERY_EYE",(15,-46,22.0),(59,-2,31),26)
camera("MAKER_OPEN_FACADE",(190,-12,110),(35,-35,60),35)
new.camera=map_["M37L_CAMERA_MAKER_EYE"]
new.render.engine="CYCLES"
new.cycles.samples=4
new.cycles.max_bounces=4
new.render.resolution_x=640
new.render.resolution_y=400
new.render.resolution_percentage=100
new.render.image_settings.file_format="PNG"
out=OUT/"M37N_MAKER_SHELL_DIRECT_EDIT_ART_HOLD.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()))
renders={}
for key,obj in {
 "MAKER_FIXED":map_["M37L_CAMERA_MAKER_EYE"],
 "AERIAL_FIXED":map_["M37L_CAMERA_AERIAL"],
 "PUBLIC_FIXED":map_["M37L_CAMERA_PUBLIC_EYE"],
 "VISITOR_SUPPLEMENTAL":new.objects["M37N_CAMERA_VISITOR_GALLERY_EYE"],
 "EXTERIOR_SUPPLEMENTAL":new.objects["M37N_CAMERA_MAKER_OPEN_FACADE"]}.items():
    new.camera=obj
    image=OUT/("M37N_"+key+".png")
    new.render.filepath=str(image.resolve())
    bpy.ops.render.render(write_still=True,scene=SCENE)
    assert image.stat().st_size>3000,key
    renders[key]={"file":image.name,"sha256":sha(image)}
    print("M37N_REAL_NATIVE_RENDER",key,flush=True)
manifest={
 "schema":"g4c7-m37n-bounded-native-carve-and-controlled-view-study-v1",
 "art":"HOLD_UNREVIEWED","official_adoption":0,
 "formal_331_993":"NOT_RUN","Minecraft":"FORBIDDEN",
 "reference_scenes":["M37L_SINGLE_CITY_MASTER_AUTHOR_ART_HOLD","M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD"],
 "source_blend_sha256":sha(SOURCE),
 "new_scene":SCENE,"copies_of_source_meshes":199,
 "source_shell_direct_mesh_cuts":cut_names,
 "shell_cut_count":len(cut_names),
 "source_mesh_material_only_change":barrier_name,
 "glazing":{"Transmission_Weight":.995,"IOR":1.07,"transparent_at_final_render":"TO_BE_JUDGED"},
 "new_visitors_physical_meshes":len(extra),
 "new_floor_access":"NOT_CERTIFIED","new_pier_structure":"NOT_CERTIFIED",
 "new_cameras":["VISITOR_GALLERY_EYE","MAKER_OPEN_FACADE"],
 "fixed_cameras_unmodified":9,
 "native_blend":{"file":out.name,"sha256":sha(out),"bytes":out.stat().st_size},
 "same_native_blend_renders":renders,
 "limits":"Local subtractive editing trial. Retains 199 initial copied meshes and sealed factory divider; does not fix overall tubular city, human walking, privacy, fire or sitewide art quality.",
}
(OUT/"M37N_AUTHOR_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print("M37N_ART_HOLD_NATIVE_SAVED",json.dumps({"sha":sha(out),"cuts":len(cut_names),"new_objects":len(extra)}),flush=True)
