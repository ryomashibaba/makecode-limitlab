"""Independent audit of saved native and GLB triangles; no builder import.
Not formal 331/993, continuous body sweep, structure or daylight simulation.
Every negative control adds/removes actual saved-scene geometry, not a JSON flag.
Usage: blender -b -t 8 -P audit_p2b.py -- B1R1 or B2R1
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
audit_args=sys.argv[sys.argv.index('--')+1:]
V=audit_args[0]; O=R/V
report=O/(audit_args[1] if len(audit_args)>1 else 'independent_mesh_audit.json')
if report.exists(): raise RuntimeError('Append-only evidence: choose a new report filename')

def signature():
    out={}
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.name.startswith('CONTEXT'): continue
        me=ob.data; me.calc_loop_triangles()
        vs=[ob.matrix_world@v.co for v in me.vertices]
        out[ob.name]={'triangles':len(me.loop_triangles),'bounds':[[min(v[a] for v in vs) for a in range(3)],[max(v[a] for v in vs) for a in range(3)]]}
    return out
def bvh(exclude=()):
    vs=[]; fs=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or ob.name.startswith('CONTEXT') or ob.name in exclude: continue
        ob.data.calc_loop_triangles(); off=len(vs)
        vs.extend(ob.matrix_world@v.co for v in ob.data.vertices)
        fs.extend(tuple(off+i for i in f.vertices) for f in ob.data.loop_triangles)
    return BVHTree.FromPolygons(vs,fs,all_triangles=True)
def hit(tree,origin,direction,distance):
    loc,normal,index,d=tree.ray_cast(Vector(origin),Vector(direction).normalized(),distance)
    return None if loc is None else {'position':list(loc),'distance':d}
def clear(tree,a,b):
    d=Vector(b)-Vector(a)
    return hit(tree,a,d,d.length) is None
def floor_at(tree,x,y,z):
    h=hit(tree,(x,y,z+.08),(0,0,-1),.16)
    return h is not None and abs(h['position'][2]-z)<.025
def box(name,lo,hi):
    bpy.ops.mesh.primitive_cube_add(size=1,location=tuple((lo[i]+hi[i])/2 for i in range(3)))
    ob=bpy.context.object; ob.name=name; ob.scale=tuple(hi[i]-lo[i] for i in range(3)); bpy.context.view_layer.update(); return ob
def stair_samples():
    pts=[]
    for y0,run,z0,rise in [(0,16.8,0,10),(18,10.2,10,6)]:
        n=math.ceil(rise/.18)
        for i in range(n): pts.append((-25,y0+(i+.5)*run/n,z0+(i+1)*rise/n))
    return pts
def evaluate(tree):
    tests={}
    tests['making_floor']=floor_at(tree,5,5,0)
    tests['research_floor']=floor_at(tree,-8,12,10)
    tests['home_floor']=floor_at(tree,-10,6,16)
    for name,p,z in [('making',(-12,6,4),9.35),('research',(-8,12,12),15.35),('home',(-10,6,18),21.5)]:
        h=hit(tree,p,(0,0,1),30)
        tests[name+'_actual_roof']=h is not None and abs(h['position'][2]-z)<.025
    tests['home_actual_privacy_wall']=hit(tree,(-10,6,18),(0,1,0),14) is not None
    tests['real_entry_open']=clear(tree,(0,-10,3),(0,8,3))
    tests['research_sees_making']=clear(tree,(-3.7,12,11.65),(13,17,5.6))
    tests['original_research_camera_sees_making']=clear(tree,(-8,12,11.65),(10,17,4))
    tests['home_south_light_aperture']=clear(tree,(-10,6,18),(-10,-60,31))
    tests['making_sky_through_roof_court']=clear(tree,(8,14,2),(8,14,120))
    tests['home_second_direction_aperture']=clear(tree,(-3.7,12,18), (35,12,22))
    # Axis centre rays do not prove width or volume clearance. Transverse samples
    # add limited width evidence, still not a formal occupancy/continuous sweep.
    axisA=[]; axisB=[]
    for offset in [-8,0,8]:
        axisA.append(clear(tree,(-280,-32+offset,3.25),(280,-32+offset,3.25)))
        axisB.append(clear(tree,(-99+offset,-242,3.25),(166+offset,240,3.25)))
    tests['axis_A_3_actual_mesh_rays']=all(axisA)
    tests['axis_B_3_actual_mesh_rays']=all(axisB)
    street=[(0,-18+i*.5,0) for i in range(70)]
    stairs=stair_samples()
    route=[(-25,17,10),(-22,17,10),(-22,18,10),(-25,18,10),(-25,28.4,16),(-21,29,16),(-21,22,16),(-22,19,16),(-22,17,16)]
    supports=[floor_at(tree,*p) for p in street+stairs+route]
    bodies=[clear(tree,(x,y,z+.15),(x,y,z+3.25)) for x,y,z in stairs]
    tests['local_route_floor_samples']=all(supports)
    tests['local_stair_vertical_body_segments']=all(bodies)
    return {'tests':tests,'floor_samples':len(supports),'floor_missing':sum(not x for x in supports),'stair_body_segments':len(bodies),'stair_body_obstructions':sum(not x for x in bodies),'axis_ray_results':[axisA,axisB]}

bpy.ops.wm.open_mainfile(filepath=str(O/(V+'.blend')))
native=signature()
# Destroy native scene in this audit process; reimport from bytes on disk.
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(O/(V+'.glb')))
imported=signature(); errors=[]
if set(native)!=set(imported): errors.append('object name sets differ')
for n in set(native)&set(imported):
    if native[n]['triangles']!=imported[n]['triangles']: errors.append('triangle count '+n)
    if max(abs(native[n]['bounds'][i][j]-imported[n]['bounds'][i][j]) for i in range(2) for j in range(3))>1e-3: errors.append('bounds '+n)
tree=bvh(); baseline=evaluate(tree)
negative=[]
# Mutations are real geometry, each removed afterwards. Baseline must be true to
# count a detected failure. A pre-existing failure is never a negative-control PASS.
for label,test,lo,hi in [
 ('entry filled','real_entry_open',(-8,-3,0),(8,0,7)),
 ('research view blocked','research_sees_making',(-2.8,3,10),(-1.8,25,15)),
 ('home aperture bricked','home_south_light_aperture',(-28,-4,16),(-2,-1,22)),
 ('sky court capped','making_sky_through_roof_court',(-2,4,10),(18,24,11)),
 ('civic void A plugged','axis_A_3_actual_mesh_rays',(-2,-50,0),(2,-14,8)),
 ('stair body blocked','local_stair_vertical_body_segments',(-28,5,2),(-22,6,7))]:
    ob=box('NEGATIVE_'+label,lo,hi); altered=evaluate(bvh())
    negative.append({'mutation':label,'baseline':baseline['tests'][test],'mutated':altered['tests'][test],'detected':baseline['tests'][test] and not altered['tests'][test]})
    bpy.data.objects.remove(ob,do_unlink=True)
for label,test,removed in [
 ('home roof removed','home_actual_roof',['HOME_ROOF']),
 ('shared research support removed','research_floor',['SHARED_MAKING_ROOF_RESEARCH_FLOOR']),
 ('stair support removed','local_route_floor_samples',['STAIR_M_R'])]:
    altered=evaluate(bvh(removed))
    negative.append({'mutation':label,'baseline':baseline['tests'][test],'mutated':altered['tests'][test],'detected':baseline['tests'][test] and not altered['tests'][test]})
angle=math.degrees(math.acos(265/math.hypot(265,482)))
result={'study':V,'source':'Saved GLB reimported in a fresh Blender process; real triangle BVH','native_meshes':len(native),'glb_meshes':len(imported),'triangles':sum(x['triangles'] for x in imported.values()),'roundtrip_errors':errors,'axis_plan_angle_degrees':angle,'baseline':baseline,'negative_controls':negative,'negatives_detected':sum(x['detected'] for x in negative),'negative_total':len(negative),'formal_331_993':'NOT RUN','formal_G0_S1_G1_G2_G3':'NOT RUN','continuous_body_sweep':'NOT RUN','structural_fire_acoustic_privacy_daylight_simulation':'NOT RUN','district_upper_routes_envelope_weather_sealing':'NOT VERIFIED','art':'REJECT; independent visual assessment required, no promotion from checks','sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [O/(V+'.blend'),O/(V+'.glb')]}}
report.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
