#!/usr/bin/env python3
"""M37-N independent Blender reopen: source SHA and 398 old meshes preserved;
10 true shell geometry cuts; sealed worker boundary and bounded new gallery.
Negative geometric controls; no art, route or construction certification.
"""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path("artifacts/g4c7-m37m-verified-native-review-workspace-art-hold")
OUT=Path("artifacts/g4c7-m37n-shipyard-view-build")
man=json.loads((OUT/"M37N_AUTHOR_MANIFEST.json").read_text())
src=ROOT/"M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD.blend"
dst=OUT/man["native_blend"]["file"]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(src)==man["source_blend_sha256"]
assert sha(dst)==man["native_blend"]["sha256"]
def snap(scene):
    return {o.name:{
        "verts":[tuple(round(float(v),5) for v in vertex.co) for vertex in o.data.vertices],
        "faces":[tuple(f.vertices) for f in o.data.polygons],
        "basis":tuple(round(float(v),5) for row in o.matrix_basis for v in row),
        "material":[m.name if m else None for m in o.data.materials]}
        for o in scene.objects if o.type=="MESH"}
oldscenes=["M37L_SINGLE_CITY_MASTER_AUTHOR_ART_HOLD",
           "M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD"]
bpy.ops.wm.open_mainfile(filepath=str(dst.resolve()))
for scene in oldscenes:
    assert len(snap(bpy.data.scenes[scene]))==199
savedold={x:snap(bpy.data.scenes[x]) for x in oldscenes}
sc=bpy.data.scenes[man["new_scene"]]
assert sc["M37N_ART"]=="EARLY_HOLD_UNREVIEWED"
assert sc["M37N_MINECRAFT"]=="FORBIDDEN"
assert sc["M37N_FORMAL_331_993"]=="NOT_RUN"
assert sc["M37N_USER_ADOPTION"]==0
mesh={o.name:o for o in sc.objects if o.type=="MESH"}
assert len(mesh)==204,(len(mesh),sorted(mesh))
oldref=bpy.data.scenes[oldscenes[1]]
assert len([o for o in sc.objects if o.type=="CAMERA"])==11
cut_names=set(man["source_shell_direct_mesh_cuts"])
assert len(cut_names)==10
expected={"M37N_"+name for name in cut_names}
def exact_native_gap(o,origin):
    assert len(origin.data.vertices)==8 and len(origin.data.polygons)==6
    assert len(o.data.vertices)==16 and len(o.data.polygons)==12
    a=[Vector(v.co) for v in origin.data.vertices]
    for ix,(start,end) in enumerate(((0,.12),(.88,1))):
        for j,t in enumerate((start,end)):
            for k in range(4):
                index=ix*8+j*4+k
                expected=a[k].lerp(a[k+4],t)
                assert (o.data.vertices[index].co-expected).length<1e-4,(o.name,index)
    return True
for oldname in cut_names:
    exact_native_gap(sc.objects["M37N_"+oldname],
                     oldref.objects["M37M_EDIT_"+oldname])
# Every OTHER copied original mesh is geometrically and transform-identical.
oldmeshes=snap(oldref)
newmeshes=snap(sc)
for name,oldmesh in oldmeshes.items():
    newname="M37N_"+name[len("M37M_EDIT_"):]
    assert newname in newmeshes
    if newname in expected:
        continue
    assert newmeshes[newname]["verts"]==oldmesh["verts"],(name,"vertices")
    assert newmeshes[newname]["faces"]==oldmesh["faces"],(name,"faces")
    assert newmeshes[newname]["basis"]==oldmesh["basis"],(name,"transform")
# Barrier still exists physically, no permeable opening created.
glass=sc.objects["M37N_M37L_MAKER_BOUNDARY_ACTUAL_MEMBRANE"]
oldglass=oldref.objects["M37M_EDIT_M37L_MAKER_BOUNDARY_ACTUAL_MEMBRANE"]
assert len(glass.data.vertices)==len(oldglass.data.vertices)==8
assert newmeshes[glass.name]["verts"]==oldmeshes[oldglass.name]["verts"]
shader=glass.data.materials[0].node_tree.nodes["Principled BSDF"]
assert shader.inputs["Transmission Weight"].default_value>=.99
assert shader.inputs["Roughness"].default_value<=.03
floor=sc.objects["M37N_PUBLIC_MAKER_FRONTAGE_WALKING_FLOOR"]
xs=[v.co.x for v in floor.data.vertices]
ys=[v.co.y for v in floor.data.vertices]
zs=[v.co.z for v in floor.data.vertices]
assert max(xs)<=min(v.co.x for v in glass.data.vertices)-.5
assert max(zs)>min(v.co.z for v in glass.data.vertices)
assert min(ys)<-53 and max(ys)>10
guards=("M37N_PUBLIC_GALLERY_SIDE_GUARD","M37N_PUBLIC_GALLERY_END_GUARD")
assert all(q in mesh for q in guards)
# 9 original fixed camera rotations and positions preserved unaltered.
for key in ("SOUTH","NORTH","AERIAL","PUBLIC_EYE","MAKER_EYE",
             "RESEARCH_EYE","HABITAT_EYE","UPPER_EYE","SKYLINE_SIDE"):
    a=oldref.objects["M37M_EDIT_M37L_CAMERA_"+key]
    b=sc.objects["M37N_M37L_CAMERA_"+key]
    assert a.location==b.location and a.rotation_euler==b.rotation_euler
    assert a.data.as_pointer()!=b.data.as_pointer()
assert len(man["same_native_blend_renders"])==5
for k,it in man["same_native_blend_renders"].items():
    png=OUT/it["file"]
    assert png.read_bytes()[:8]==b"\x89PNG\r\n\x1a\n" and sha(png)==it["sha256"]
# Failure controls work against ACTUAL saved native vertex and materials.
bad=[]
def rejected(label,fn):
    try:fn()
    except (AssertionError,ValueError):bad.append(label);return
    raise AssertionError("NEGATIVE_CONTROL_FAILED_TO_DETECT:"+label)
one=sc.objects["M37N_"+sorted(cut_names)[0]]
base=oldref.objects["M37M_EDIT_"+sorted(cut_names)[0]]
original_coords=[v.co.copy() for v in one.data.vertices]
# weld gap into old topology in memory; copy back exact new geometry without save.
def destroy_gap():
    one.data.clear_geometry()
    one.data.from_pydata([tuple(v.co) for v in base.data.vertices],[],
                         [tuple(p.vertices) for p in base.data.polygons])
    one.data.update()
    exact_native_gap(one,base)
rejected("fill_shell_aperture",destroy_gap)
one.data.clear_geometry()
one.data.from_pydata([tuple(v) for v in original_coords],[],
                     [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),
                      (11,10,9,8),(12,13,14,15),(8,9,13,12),(9,10,14,13),(10,11,15,14),(11,8,12,15)])
one.data.update()
exact_native_gap(one,base)
trans=shader.inputs["Transmission Weight"].default_value
shader.inputs["Transmission Weight"].default_value=0
rejected("opaque_workzone_glass",lambda:(
    (_ for _ in ()).throw(AssertionError("Transmission disabled"))
    if shader.inputs["Transmission Weight"].default_value<.99 else None))
shader.inputs["Transmission Weight"].default_value=trans
v=floor.data.vertices[0].co.copy()
floor.data.vertices[0].co.x+=50
rejected("public_gallery_crosses_staff_partition",lambda:(
    (_ for _ in ()).throw(AssertionError("Public deck crosses staff barrier"))
    if max(q.co.x for q in floor.data.vertices)>min(q.co.x for q in glass.data.vertices)-.5 else None))
floor.data.vertices[0].co=v
assert len(bad)==3
# Verify original saved source unaffected by this studio, after loading original source.
bpy.ops.wm.open_mainfile(filepath=str(src.resolve()))
for key in oldscenes:assert snap(bpy.data.scenes[key])==savedold[key],key
audit={
 "result":"LIMITED_NATIVE_SUBTRACTIVE_SHELL_AND_SEALED_VIEW_METHOD_PASS",
 "source_M37L_and_M37M_preserved_meshes_each":199,
 "source_scene_count_protected":2,
 "copied_source_native_meshes":199,
 "direct_modified_shell_patch_meshes":10,
 "source_barrier_still_exists":"YES_FULL_PHYSICAL_MEMBRANE",
 "glazing_optical_quality":"REQUIRES_VISUAL_REVIEW",
 "added_actual_gallery_or_guards_or_piers":5,
 "unmodified_fixed_cameras":9,"supplemental_cameras":2,
 "verified_saved_native_renders":5,
 "physical_negative_controls_rejected":bad,
 "new_city_art":"NOT_PASSED",
 "formal_331_993":"NOT_RUN",
 "interior_freely_walkable":"NOT_CERTIFIED",
 "workzone_security_and_glass_impact":"NOT_CERTIFIED",
 "structural_support":"NOT_CERTIFIED",
 "minecraft":"FORBIDDEN","official_adoption":0,
 "source_sha256":sha(src),"new_blend_sha256":sha(dst)}
(OUT/"M37N_INDEPENDENT_NATIVE_REOPEN_AUDIT.json").write_text(json.dumps(audit,indent=2,ensure_ascii=False))
print("M37N_NATIVE_AUDIT",json.dumps(audit,ensure_ascii=False),flush=True)
