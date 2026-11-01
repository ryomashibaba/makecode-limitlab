#!/usr/bin/env python3
"""G4C7 M37-F limited connected-city SECTION experiment, no art or safety pass.
Append a continuous functional ground urban artery and stair studies in an
independently duplicated Blender working scene. No changes to old scenes.
Blender-native geometry, not a 2D path guide. No Minecraft writes.
"""
import bpy, hashlib, json, math
from pathlib import Path
from mathutils import Vector
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

ROOT=Path('artifacts/g4c7-m37d-verified-native-urban-fabric-art-hold')
OUT=Path('artifacts/g4c7-m37f-native-section-output')
OUT.mkdir(parents=True,exist_ok=True)
SOURCE=ROOT/'M37D_NEW_NATIVE_URBAN_FABRIC_ART_HOLD.blend'
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
previous=json.loads((ROOT/'M37D_MANIFEST.json').read_text())
assert sha(SOURCE)==previous['saved_blend']['sha256']
assert previous['art']=='HOLD_UNREVIEWED' and previous['minecraft']=='FORBIDDEN'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE.resolve()))
for name in ('M35_REJECTED_REFERENCE_LOCKED','M36_AUTHORING_STUDIO_ART_HOLD',
             'M37D_AUTHOR_OCCUPIED_CITY_ART_HOLD'):
    assert name in bpy.data.scenes
old=bpy.data.scenes['M37D_AUTHOR_OCCUPIED_CITY_ART_HOLD']
assert len([o for o in old.objects if o.type=='MESH'])==1163
new=bpy.data.scenes.new('M37F_CONNECTED_SECTION_METHOD_ART_HOLD')
new.world=old.world
new['SOURCE_M37D_SHA256']=sha(SOURCE)
new['M37F_SCOPE']='CIVIC_SECTION_CONNECTIVITY_METHOD_NOT_NEW_CITY_ART'
new['M37F_ART']='M37D_ART_REJECT_UNCHANGED_M37F_ART_HOLD'
new['M37F_FORMAL_331_993']='NOT_RUN'
new['M37F_OFFICIAL_ADOPTION']=0
new['M37F_MINECRAFT']='FORBIDDEN'
new['M37F_SCALE']='ABSTRACT_RESEARCH_UNITS_NOT_MINECRAFT_BLOCKS'
col=bpy.data.collections.new('M37F_ACTUAL_CIVIC_SECTION_NOT_GUIDE')
new.collection.children.link(col)
remap={}
for obj in old.objects:
    copy=obj.copy()
    if obj.data:copy.data=obj.data.copy()
    copy.name='M37F_BASE_'+obj.name
    col.objects.link(copy)
    remap[obj.name]=copy
assert len([o for o in new.objects if o.type=='MESH'])==1163
assert all(remap[o.name].data.as_pointer()!=o.data.as_pointer()
           for o in old.objects if o.type=='MESH')

material=bpy.data.materials.new('M37F_PUBLIC_PAVING_COPPER')
material.diffuse_color=(.52,.47,.38,1)
material.use_nodes=True
material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.52,.47,.38,1)
structure=bpy.data.materials.new('M37F_STAIR_BODY_DARK_STONE')
structure.diffuse_color=(.36,.42,.43,1)
structure.use_nodes=True
structure.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.36,.42,.43,1)
counts={'ground_road_segments':0,'flight_treads':0,'flight_landings':0,'ground_landings':0}
added=[]

def prism(name,polygon,z0,z1,mat,role):
    assert len(polygon)>=3 and z1>z0
    verts=[(float(x),float(y),float(z)) for z in (z0,z1) for x,y in polygon]
    n=len(polygon)
    # All footprint pieces below are convex quadrilaterals.
    assert n==4
    faces=[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new('M37F_'+name+'_data')
    mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('M37F_'+name,mesh)
    col.objects.link(obj)
    mesh.materials.append(mat)
    obj['M37F_ROLE']=role
    obj['M37F_ART']='HOLD_NOT_CERTIFIED'
    added.append(obj)
    return obj

def route_segment(name,a,b,width=14.0,top=.15):
    dx=b[0]-a[0];dy=b[1]-a[1]
    d=math.hypot(dx,dy)
    assert d>1
    ux,uy=dx/d,dy/d
    nx,ny=-uy,ux
    # Two-meter overlaps at either end prevent merely line-touching seams.
    polygon=[(a[0]-2*ux-width/2*nx,a[1]-2*uy-width/2*ny),
             (b[0]+2*ux-width/2*nx,b[1]+2*uy-width/2*ny),
             (b[0]+2*ux+width/2*nx,b[1]+2*uy+width/2*ny),
             (a[0]-2*ux+width/2*nx,a[1]-2*uy+width/2*ny)]
    o=prism(name,polygon,top-.45,top,material,'GROUND_PUBLIC_PHYSICAL_FLOOR_NOT_CERTIFIED')
    counts['ground_road_segments']+=1
    return o

def square(name,x,y,width,top=.15):
    w=width/2
    o=prism(name,[(x-w,y-w),(x+w,y-w),(x+w,y+w),(x-w,y+w)],
            top-.45,top,material,'ACTUAL_LANDING_PHYSICAL_FLOOR_NOT_CERTIFIED')
    counts['ground_landings']+=1
    return o

routes={
 'GATE_TO_YARD':[(-9,-125),(-9,-88),(-2,-54),(42,-51),(91,-43)],
 'GATE_TO_HABITAT':[(-12,-86),(-25,-43),(-62,-20),(-105,-24)],
 'GATE_TO_CULTURE':[(-9,-130),(-52,-132),(-111,-130)],
 'CIVIC_TO_RESEARCH':[(-13,-53),(-13,20),(-8,73),(18,92),(62,112)],
}
anchors={'GATE':(-10,-118),'CIVIC':(-9,-72),'DELTA':(-11,20),
         'NORTH_HALL':(-4,80),'SHIPYARD':(95,-42),'HABITAT':(-103,-24),
         'CULTURE':(-108,-128),'RESEARCH':(61,111)}
planned=unary_union([LineString(points).buffer(7,resolution=4)
                     for points in routes.values()])
assert planned.is_valid and planned.geom_type=='Polygon'
assert all(planned.covers(Point(point)) for point in anchors.values())
for label,points in routes.items():
    for i,(a,b) in enumerate(zip(points,points[1:])):
        route_segment(label+'_SEG_%02d'%i,a,b)
# Public court connector polygon physically co-located with old plaza.
for name,x,y,w in [('GATE',-9,-125,18),('CIVIC',-9,-88,18),
                   ('DELTA',-13,20,18),('NORTH',-8,73,18),
                   ('YARD',91,-43,22),('HAB',-105,-24,18),
                   ('CULTURE',-111,-130,18),('RESEARCH',62,112,22)]:
    square(name+'_PUBLIC_PAVED_ARRIVAL',x,y,w)

# True native tread geometry, not non-renderable guides. The upper stair
# remains a conceptual trajectory; centerline full body QA NOT DONE.
def stair(name,a,b,ztop0,ztop1,n,width):
    assert n>0 and ztop1>ztop0
    dx=b[0]-a[0];dy=b[1]-a[1]
    length=math.hypot(dx,dy)
    ux,uy=dx/length,dy/length
    nx,ny=-uy,ux
    run=length/n
    for i in range(n):
        # Positive end-face overlap makes actual solid floor, each tread's
        # top elevation rises; vertical riser is real mesh below tread.
        u0=(i-.04)*run;u1=(i+1.04)*run
        poly=[(a[0]+ux*u0-nx*width/2,a[1]+uy*u0-ny*width/2),
              (a[0]+ux*u1-nx*width/2,a[1]+uy*u1-ny*width/2),
              (a[0]+ux*u1+nx*width/2,a[1]+uy*u1+ny*width/2),
              (a[0]+ux*u0+nx*width/2,a[1]+uy*u0+ny*width/2)]
        top=ztop0+(ztop1-ztop0)*(i+1)/n
        prism(name+'_TREAD_%03d'%i,poly,top-.30,top,
              structure,'UPWARD_NATIVE_TREAD_NOT_SWEEP_CERTIFIED')
        counts['flight_treads']+=1
    # Stair landing near top must co-locate with actual existing activity floor.
    square(name+'_DEST_LANDING',b[0],b[1],width+4,top=ztop1)
    counts['ground_landings']-=1
    counts['flight_landings']+=1
    return {'from':a,'to':b,'z_top_start':ztop0,'z_top_end':ztop1,
            'treads':n,'nominal_rise':(ztop1-ztop0)/n,
            'nominal_run':length/n,
            'claim':'concept only; support, landing and clearance not certified'}

# Research ground floor in source scene is z=4, upper observation is z=22.1.
# These are independent design stair corridors, NOT certified walkable.
stairs={
 'RESEARCH_ACCESS':stair('RESEARCH_ACCESS',(18,92),(62,112),.15,4.225,17,6),
 'UPPER_ACCESS':stair('UPPER_ACCESS',(-8,73),(17,124),.15,22.35,89,6),
}

# Preserve all original nine camera positions and make five meaningful
# research views at actual new gate, road, stair, yard and aerial locations.
camera_keys=('SOUTH','NORTH','AERIAL','STREET','YARD','HAB_EYE','RESEARCH_EYE','CULTURE_EYE','UPPER_EYE')
assert all('M37D_CAM_'+key in remap for key in camera_keys)
old_cameras={key:remap['M37D_CAM_'+key] for key in camera_keys}

def author_camera(name,loc,target,lens=22):
    cd=bpy.data.cameras.new('M37F_CAMERA_'+name+'_lens')
    ob=bpy.data.objects.new('M37F_CAMERA_'+name,cd)
    col.objects.link(ob)
    ob.location=loc
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    cd.lens=lens
    return ob
cams={
 'SOUTH':old_cameras['SOUTH'],
 'AERIAL':old_cameras['AERIAL'],
 'STREET_OLD':old_cameras['STREET'],
 'CULTURE_EYE_OLD':old_cameras['CULTURE_EYE'],
 'GROUND_GATE':author_camera('GROUND_GATE',(-8,-143,2.7),(-9,-65,3.3)),
 'SPINE_CIVIC':author_camera('SPINE_CIVIC',(-14,-60,2.7),(-8,27,8)),
 'SHIPYARD_APPROACH':author_camera('SHIPYARD_APPROACH',(36,-52,3), (107,-30,12)),
 'RESEARCH_STAIR':author_camera('RESEARCH_STAIR',(11,89,3), (56,116,10)),
 'HIGH_ROUTE':author_camera('HIGH_ROUTE',(-6,75,3), (17,124,30)),
}
new.camera=cams['SOUTH']
new.render.engine='CYCLES'
new.cycles.samples=7
new.render.resolution_x=760;new.render.resolution_y=456
new.render.resolution_percentage=100
new.render.image_settings.file_format='PNG'
# All added route geometry is new, and all source scene geometry is pinned.
assert len(added)==counts['ground_road_segments']+counts['ground_landings']+counts['flight_treads']+counts['flight_landings']
new['M37F_SAVED_NEW_OBJECT_COUNT']=len(added)
new['M37F_ROUTES_REAL_MESH']=json.dumps(routes)
new['M37F_ROUTE_AUDIT']='NOT_FORMAL_SAFETY'
if bpy.context.window:bpy.context.window.scene=new
path=OUT/'M37F_NATIVE_CIVIC_SECTION_ART_HOLD.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(path.resolve()))
renderings={}
for key,cam in cams.items():
    new.camera=cam
    img=OUT/('M37F_'+key+'.png')
    new.render.filepath=str(img.resolve())
    bpy.ops.render.render(write_still=True,scene=new.name)
    assert img.exists() and img.stat().st_size>5000
    renderings[key]={'file':img.name,'sha256':sha(img)}
    print('M37F_SAVED_FIXED_VIEW',key,flush=True)
manifest={
 'study':'M37F_NATIVELY_EDITED_CIVIC_ROUTE_SECTION_NOT_CITY_ART_PASS',
 'source_blend_sha256':sha(SOURCE),
 'saved_blend':{'file':path.name,'sha256':sha(path),'bytes':path.stat().st_size},
 'source_scenes_untouched':['M35_REJECTED_REFERENCE_LOCKED','M36_AUTHORING_STUDIO_ART_HOLD','M37D_AUTHOR_OCCUPIED_CITY_ART_HOLD'],
 'new_scene':new.name,'source_meshes_cloned':1163,
 'new_native_mesh_counts':counts,'new_native_total_meshes':len(added),
 'planned_ground_route_control_points':routes,
 'anchors':anchors,'stairs':stairs,
 'cameras':renderings,
 'baseline_art':'M37D_ART_REJECT','new_art':'HOLD_NOT_EVALUATED',
 'continuous_walkable_route':'NOT_CERTIFIED',
 'formal_331_993':'NOT_RUN','G0_S1_G1_G2_G3':'NOT_RUN',
 'minecraft':'FORBIDDEN','construction_writes':0,
 'important':'Nominal stairs and real route slabs are not a safe continuous human path. Final ART adoption 0.'}
(OUT/'M37F_NATIVE_SECTION_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
print('M37F_NATIVE_SECTION_SAVED',json.dumps({'source_sha':sha(SOURCE),'new_meshes':len(added),'render_count':len(renderings),'sha':sha(path)},ensure_ascii=False),flush=True)
