#!/usr/bin/env python3
"""Construct tiny bounded native Blender METHOD fixture, NOT a city or art candidate.
All shapes come from the validated semantic state; west-author edit affects both
actual room floors and envelope-facing walls. Does not edit old M35-M37J files.
"""
import bpy, json, hashlib, sys
from pathlib import Path
from g4c7_m37k_author_kernel import initial_state, apply_transaction, validate, exterior_outline

OUT=Path('artifacts/g4c7-m37k-native-method-fixture')
OUT.mkdir(parents=True,exist_ok=True)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

initial=initial_state();state=apply_transaction(initial,{'op':'MOVE_SHARED_WEST_FACADE','delta':-2.0})
result=validate(state)
assert result['valid']

# Avoid leaking Blender's default scene into the evidence.
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.name='M37K_EDITABLE_SECTION_WORKBENCH_METHOD_ONLY'
scene['M37K_ART']='HOLD_NOT_AN_ART_CANDIDATE'
scene['M37K_FORMAL_331_993']='NOT_RUN'
scene['M37K_MC']='FORBIDDEN'
scene['M37K_OFFICIAL_ADOPTION']=0
scene['M37K_AUTHOR_TRANSACTION']='MOVE_SHARED_WEST_FACADE=-2.0'
scene['M37K_UNITS']='ABSTRACT_RESEARCH_UNITS'

palette={
 'PUBLIC_FLOOR':(.43,.55,.56), 'MAKER_FLOOR':(.41,.44,.49),
 'PUBLIC_WALL':(.58,.53,.42), 'MAKER_WALL':(.31,.40,.43),
 'GALLERY':(.62,.48,.34), 'STAIR':(.8,.67,.39),
 'GLASS':(.16,.66,.73), 'EXTERIOR':(.34,.39,.42)}
mats={}
for role,rgb in palette.items():
    m=bpy.data.materials.new('M37K_'+role)
    m.diffuse_color=(*rgb,1)
    m.use_nodes=True
    bsdf=m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=(*rgb,1)
    bsdf.inputs['Roughness'].default_value=.55
    if role=='GLASS':
        bsdf.inputs['Metallic'].default_value=.0
        bsdf.inputs['Roughness'].default_value=.12
    mats[role]=m

def box(name,x0,y0,z0,x1,y1,z1,role):
    assert min(x1-x0,y1-y0,z1-z0)>1e-5,(name,x0,y0,z0,x1,y1,z1)
    vs=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
        (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    fs=[(3,2,1,0),(4,5,6,7),(0,1,5,4),
        (1,2,6,5),(2,3,7,6),(3,0,4,7)]
    mesh=bpy.data.meshes.new(name+'_mesh')
    mesh.from_pydata(vs,[],fs)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    scene.collection.objects.link(ob)
    mesh.materials.append(mats[role])
    ob['M37K_ROLE']=role
    ob['M37K_GEOMETRY']='ACTUAL_SOLID_GEOMETRY_NOT_GUIDE'
    return ob

p=state['rooms']['CIVIC']['bounds'];m=state['rooms']['MAKER']['bounds'];g=state['rooms']['GALLERY']['bounds']
box('M37K_CIVIC_ROOM_ACTUAL_FLOOR',p[0],p[1],-.4,p[2],p[3],0.,'PUBLIC_FLOOR')
box('M37K_MAKER_ROOM_ACTUAL_FLOOR',m[0],m[1],-.4,m[2],m[3],0.,'MAKER_FLOOR')
# This west exterior is changed by the same authored input as the interior.
box('M37K_CIVIC_WEST_EXTERIOR_WALL',p[0]-.22,p[1],0.,p[0],p[3],8.,'EXTERIOR')
box('M37K_GALLERY_WEST_EXTERIOR_WALL',g[0]-.22,g[1],8.,g[0],g[3],16.,'EXTERIOR')
box('M37K_CIVIC_NORTH_WALL',p[0],p[3]-.2,0.,p[2],p[3],8.,'PUBLIC_WALL')
box('M37K_MAKER_NORTH_WALL',m[0],m[3]-.2,0.,m[2],m[3],12.,'MAKER_WALL')
box('M37K_MAKER_EAST_WALL',m[2]-.2,m[1],0.,m[2],m[3],12.,'MAKER_WALL')
box('M37K_MAKER_SOUTH_WALL',m[0],m[1],0.,m[2],m[1]+.2,12.,'MAKER_WALL')
# CIVIC south wall: real gate aperture x[-5.8,-3.0], z[0,3.7]
entry=next(x for x in state['ports'] if x['id']=='P_VISITOR_GATE')
g0,g1=entry['interval'];z0,z1=entry['z']
box('M37K_PUBLIC_GATE_LEFT_SOLID',p[0],p[1]-.2,0.,g0,p[1],8.,'PUBLIC_WALL')
box('M37K_PUBLIC_GATE_RIGHT_SOLID',g1,p[1]-.2,0.,p[2],p[1],8.,'PUBLIC_WALL')
box('M37K_PUBLIC_GATE_ACTUAL_LINTEL',g0,p[1]-.2,z1,g1,p[1],8.,'PUBLIC_WALL')
# Shared wall x=0 has REAL geometric gap but sealed by solid glass membrane.
view=next(x for x in state['ports'] if x['id']=='P_MAKER_VIEW')
y0,y1=view['interval'];v0,v1=view['z']
box('M37K_MAKER_BOUNDARY_SOUTH_SOLID',-.18,p[1],0.,.18,y0,8.,'MAKER_WALL')
box('M37K_MAKER_BOUNDARY_NORTH_SOLID',-.18,y1,0.,.18,p[3],8.,'MAKER_WALL')
box('M37K_MAKER_BOUNDARY_VIEW_SILL',-.18,y0,0.,.18,y1,v0,'MAKER_WALL')
box('M37K_MAKER_BOUNDARY_VIEW_HEADER',-.18,y0,v1,.18,y1,8.,'MAKER_WALL')
box('M37K_CONTROLLED_VIEW_MEMBRANE',-.08,y0,v0,.08,y1,v1,'GLASS')
# Four actual solid slab pieces around an entirely missing rectangular hole.
# No hidden uncut solid upper-floor plane under the shaft.
slot=state['upper_slot'];sx0,sx1=slot['x'];sy0,sy1=slot['y']
# Left/right strips extend full y, northern cap fills rest.
box('M37K_UPPER_FLOOR_LEFT',g[0],g[1],7.70,sx0,g[3],8.,'GALLERY')
box('M37K_UPPER_FLOOR_RIGHT',sx1,g[1],7.70,g[2],g[3],8.,'GALLERY')
box('M37K_UPPER_FLOOR_NORTH_CAP',sx0,sy1,7.70,sx1,g[3],8.,'GALLERY')

# Real stair mesh generated from the *same* spec and slot, not independently.
stair=state['stairs'];tread_names=[]
for idx in range(stair['treads']):
    ystart=stair['y0']+(stair['y1']-stair['y0'])*idx/stair['treads']
    yend=stair['y0']+(stair['y1']-stair['y0'])*(idx+1)/stair['treads']
    top=stair['z0']+(stair['z1']-stair['z0'])*(idx+1)/stair['treads']
    name=f'M37K_STAIR_TREAD_{idx:02d}'
    box(name,stair['center_x']-stair['width']/2,ystart,top-.20,
        stair['center_x']+stair['width']/2,yend,top,'STAIR')
    tread_names.append(name)

# Capture actual native scene from a fixed set of cameras; no art judgment.
world=bpy.data.worlds.new('M37K_neutral_world')
scene.world=world;world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.45,.52,.6,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.7
from mathutils import Vector
cams={
 'SECTION_AERIAL':((-35,-33,29),(-1,0,4),33),
 'PUBLIC_GATE_EYE':((-4.5,-22,2.1),(-4.5,0,4),28),
 'SEALED_VIEW_EYE':((-5.0,0,2.7),(2,0,3),33),
 'UPPER_SLOT':((-20,13,22),(-4.5,2,7),34)}
for name,(pos,target,lens) in cams.items():
    data=bpy.data.cameras.new('M37K_'+name)
    ob=bpy.data.objects.new('M37K_CAM_'+name,data)
    scene.collection.objects.link(ob)
    ob.location=pos
    ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    data.lens=lens
area=bpy.data.lights.new('M37K_AREA','AREA')
area.energy=6500;area.size=35
light=bpy.data.objects.new('M37K_AREA_LIGHT',area)
scene.collection.objects.link(light)
light.location=(-12,-12,30)
light.rotation_euler=(Vector((0,0,5))-light.location).to_track_quat('-Z','Y').to_euler()
scene.render.engine='CYCLES';scene.cycles.samples=8
scene.render.resolution_x=800;scene.render.resolution_y=500
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'

blend=OUT/'M37K_NATIVE_AUTHORING_METHOD_ONLY_ART_HOLD.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(blend.resolve()))
render_sha={}
for label in cams:
    scene.camera=scene.objects['M37K_CAM_'+label]
    dst=OUT/f'M37K_{label}.png'
    scene.render.filepath=str(dst.resolve())
    bpy.ops.render.render(write_still=True,scene=scene.name)
    assert dst.exists() and dst.stat().st_size>1500
    render_sha[label]={'file':dst.name,'sha256':sha(dst)}
manifest={'schema':'g4c7-m37k-native-authoring-fixture-v1',
    'native_blend':{'name':blend.name,'bytes':blend.stat().st_size,'sha256':sha(blend)},
    'baseline_exterior':exterior_outline(initial),
    'edited_exterior':exterior_outline(state),
    'canonical_author_state':state,
    'native_room_floors':2,'upper_floor_actual_solid_pieces':3,
    'physical_glazing_barriers':1,'public_real_wall_openings':1,
    'native_stair_treads':len(tread_names),
    'renders':render_sha,'art':'ART_HOLD_NOT_A_CITY',
    'formal_331_993':'NOT_RUN','minecraft':'FORBIDDEN','adoption':0,
    'blender_method':'AUTHOR_DIRECTED_SEMANTIC_TRANSACTION_TO_NATIVE_GEOMETRY',
    'is_manual_GUI_edit':False}
(OUT/'M37K_NATIVE_AUTHOR_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print('M37K_NATIVE_METHOD_BUILT',json.dumps({'blend_sha':sha(blend),'images':len(render_sha),
    'glazing_count':1,'real_upper_floor_hole':True,'treads':len(tread_names)},ensure_ascii=False),flush=True)
