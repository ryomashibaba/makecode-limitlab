#!/usr/bin/env python3
"""M24 ART-FIRST inhabitable civic ridge, using the SHA-pinned M22 native scene.
New architectural study is a distinct editable collection; legacy art stays intact
but render-hidden. No city adoption or Minecraft construction authority.
"""
import hashlib, json, math, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/'artifacts/m24_immutable_m22'
SPEC=ROOT/'research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json'
OUT=ROOT/'artifacts/g4c7-m24-single-integrated-hero-landmark'/('run_'+os.getenv('GITHUB_SHA','local')[:12])
PIN='22473a0d17fb59470049fb22b508dcfc294316185d38878b5563e213246af9df'
CAMERAS={
 'south':((9,-155,82),(0,-2,25),38),
 'north':((34,141,100),(-6,8,30),36),
 'oblique':((-152,-96,103),(-4,8,27),36),
 'district':((161,-49,105),(-3,11,31),36),
 'street_eye':((4,-57,2.1),(-8,7,18),28),
 'maker_eye':((-42,-20,2.0),(-23,4,10),23),
 'research_eye':((-34,38,47.5),(-32,19,47),28),
 'resident_eye':((30,43,55),(24,24,54),28)}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def source():
 files=list(SEED.rglob('M22_EDITABLE_REVISED_PUBLIC_ROUTE.blend'))
 assert len(files)==1,('Need one original M22',len(files))
 assert sha(files[0])==PIN,'Source SHA mismatch'
 return files[0]
def preflight():
 s=json.loads(SPEC.read_text(encoding='utf-8'))
 assert len(s['nodes'])==18 and len(s['edges'])==18
 assert s['gates']['art']=='HOLD' and s['gates']['minecraft_education']=='NO_WRITE'
 assert len(CAMERAS)==8
 assert not OUT.exists(),'No output overwrite'
 return {'original_M22':str(source()),'M17_nodes':18,'study':'M24_ART_FIRST_UNAPPROVED'}
def run():
 import bpy
 from mathutils import Vector
 report=preflight()
 bpy.ops.wm.open_mainfile(filepath=str(source().resolve()))
 scene=bpy.context.scene
 old=set(bpy.data.objects)
 existing_road=bpy.data.objects.get('M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD')
 assert existing_road is not None and existing_road.type=='MESH'
 for o in old:
  if o!=existing_road:o.hide_render=True
 c=bpy.data.collections.new('M24_ONE_INTEGRATED_INHABITED_CIVIC_LANDMARK')
 scene.collection.children.link(c)
 def link(o):
  for prev in list(o.users_collection):prev.objects.unlink(o)
  c.objects.link(o)
  return o
 def mat(name,col,metal=0,rough=.45,glass=0,glow=0):
  m=bpy.data.materials.new('M24_'+name);m.use_nodes=True;m.diffuse_color=(*col,1)
  p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*col,1)
  p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
  p.inputs['Transmission Weight'].default_value=glass
  if glow:
   p.inputs['Emission Color'].default_value=(*col,1)
   p.inputs['Emission Strength'].default_value=glow
  return m
 M={
 'chalk':mat('warm white ceramic concrete',(.69,.72,.68),.08),
 'limestone':mat('amber dune limestone',(.54,.51,.43)),
 'bronze':mat('bronze load-bearing frame',(.30,.25,.19),.61,.31),
 'copper':mat('oxidized copper fins',(.17,.37,.34),.35),
 'inner':mat('buttercream interior wall',(.83,.76,.61)),
 'wood':mat('interior human scale timber',(.42,.26,.13)),
 'glass':mat('clear blue-green glazed window',(.39,.67,.67),.04,.14,.72),
 'green':mat('planted vegetation',(.09,.32,.21)),
 'leaf2':mat('garden mixed planting',(.22,.42,.26)),
 'soil':mat('planted rooftop raised bed',(.35,.29,.22)),
 'gold':mat('warm low-power lantern',(.93,.76,.47),0,.38,0,1.6),
 'cloth':mat('market shade textile',(.70,.44,.32)),
 'river':mat('courtyard water surface',(.27,.48,.51),.18,.22,.38),
 }
 new=[]
 def cube(name,xyz,sz,m,bevel=0,rot=0):
  bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
  o=bpy.context.object;o.name='M24_'+name;o.dimensions=sz
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  link(o);o.data.materials.append(M[m]);new.append(o)
  if rot:o.rotation_euler.z=rot
  if bevel:
   mod=o.modifiers.new('Soft_exposed_edge','BEVEL');mod.width=bevel;mod.segments=2
   o.modifiers.new('Weighted_normal','WEIGHTED_NORMAL')
  return o
 def beam(name,a,b,diam,m):
  x,y=Vector(a),Vector(b);v=y-x
  o=cube(name,tuple((x+y)*.5),(diam,diam,v.length),m,.075)
  o.rotation_euler=v.to_track_quat('Z','Y').to_euler()
  return o
 def surface(name,poly,z,thickness,m):
  data=bpy.data.meshes.new('M24_'+name+'_poly')
  data.from_pydata([(x,y,z) for x,y in poly],[],[tuple(range(len(poly)))])
  data.update();ob=bpy.data.objects.new('M24_'+name,data);c.objects.link(ob)
  ob.data.materials.append(M[m]);new.append(ob)
  mod=ob.modifiers.new('Structural_thickness','SOLIDIFY');mod.thickness=thickness
  mod.offset=0
  return ob
 def disk(name,xyz,r,height,m,verts=12):
  bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=height,location=xyz)
  o=bpy.context.object;o.name='M24_'+name;link(o);o.data.materials.append(M[m]);new.append(o);return o
 def vegetation(prefix,x,y,z,scale=1):
  disk(prefix+'_basin',(x,y,z+.6*scale),1.3*scale,.9*scale,'soil')
  disk(prefix+'_trunk',(x,y,z+2.1*scale),.19*scale,3.1*scale,'wood',10)
  for i,(dx,dy,dz,r) in enumerate(((0,0,4.8,2.2),(-1.1,.3,4.1,1.7),(.8,-.6,4.5,1.9))):
   bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=r*scale,
       location=(x+dx*scale,y+dy*scale,z+dz*scale))
   o=bpy.context.object;o.name='M24_'+prefix+'_leaf'+str(i);link(o)
   o.data.materials.append(M['green' if i!=1 else 'leaf2']);new.append(o)
 def stair(name,a,b,z0,z1,width,steps=48):
  # Visually real 48 distinct ascending treads, not certified walkability.
  ax,ay=a;bx,by=b;dx=bx-ax;dy=by-ay;L=math.hypot(dx,dy)
  yaw=math.atan2(dy,dx);tread=L/steps
  for i in range(steps):
   t=(i+.5)/steps
   x=ax+dx*t;y=ay+dy*t;z=z0+(i+.5)*(z1-z0)/steps
   cube(name+'_step_%02d'%i,(x,y,z),(.85*tread,width,.19), 'chalk',.015,rot=yaw)
  for side in (-1,1):
   px=-dy/L*side*width*.48;py=dx/L*side*width*.48
   beam(name+'_guard_'+str(side),(ax+px,ay+py,z0+1.15),(bx+px,by+py,z1+1.15),.14,'bronze')
 # M24: ONE integrated split-ridge civic landmark. M22 genuine public street
 # preserved, ART REJECT M24 massing is NEVER imported into this new scene.
 # Two INHABITED banks and a sky-open negative-space public atrium.
 west=[(9.6,-63,-14,10,59),(27,-65,-14,18,66),(46,-59,-15,25,70),(68,-53,-18,32,76)]
 east=[(9.6,12,58,4,56),(30,10,58,12,64),(53,12,54,20,70),(79,16,49,27,74)]
 # Underlying heritage route remains untouched. New daylight atrium surrounds it.
 surface('sky_open_atrium_court',[(-15,-11),(13,-12),(16,37),(-16,43)],.16,.4,'limestone')
 cube('civic_water_rill',(1,12,.45),(3.2,26,.13),'river',.05)
 for i,(x,y) in enumerate(((-9,15),(8,26))):vegetation('sunken_court_tree_%d'%i,x,y,.4,.83)
 surface('visible_maker_ground',[(-69,-29),(-14,-29),(-14,13),(-69,12)],.18,.70,'chalk')
 for i,(x,y) in enumerate(((-51,-17),(-34,-18),(-55,-4),(-36,1))):
  cube('maker_visible_equipment_%d'%i,(x,y,1.1),(7,3.4,1.8),'bronze',.17)
  cube('maker_real_workpiece_%d'%i,(x,y,2.05),(3.1,1.9,.20),'copper',.04)
  cube('maker_human_worktable_%d'%i,(x+3,y+3,1.0),(4,2.4,1.4),'wood',.12)
 for i,(x,y) in enumerate(((26,-43),(39,-26),(29,-8))):
  cube('public_market_bench_%d'%i,(x,y,1),(8,3.2,1.7),'wood',.18)
  cube('public_market_shelter_%d'%i,(x,y,4.7),(12,7,.38),'cloth',.10)
  for offset in (-5,5):beam('public_market_pier_%d_%d'%(i,offset),(x+offset,y-3.2,0),(x+offset,y-3.2,4.5),.28,'bronze')
 # A physical occupied unit consists of sheltered floor, human-height partitions
 # with open doors, actually visible furniture, an open courtyard glazing bay,
 # and an upper daylight canopy. Not a labelled/isolated rooftop cube.
 def inhabited_bank(side,tiers):
  for i,(z,x0,x1,y0,y1) in enumerate(tiers):
   if side=='research':
    poly=[(x0,y0+4),(x1-2,y0),(x1+1,y0+17),(x1,y1-5),
          (x0+4,y1+2),(x0-4,y1-12)]
    inner=x1;outer=x0-2
   else:
    poly=[(x0,y0+2),(x1-4,y0-5),(x1+2,y0+10),(x1+2,y1-4),
          (x1-7,y1+2),(x0+2,y1-1)]
    inner=x0;outer=x1+1
   surface(side+'_occupied_floor_%d'%i,poly,z,.8,'limestone')
   # Interior occupancy rather than a closed box parked on a slab.
   for j,xx in enumerate((x0+8,(x0+x1)/2,x1-8)):
    cube(side+'_occupied_workstation_%d_%d'%(i,j),(xx,y0+13,z+.92),(4.2,2.3,1.25),'wood',.14)
    cube(side+'_warm_tasklight_%d_%d'%(i,j),(xx,y0+13,z+1.65),(1.2,.3,.11),'gold')
   for j,yy in enumerate((y0+24,y0+39)):
    if yy>y1-8:continue
    for k,(aa,bb) in enumerate(((x0+3,x0+14),(x0+20,x1-2))):
     cube(side+'_real_partition_%d_%d_%d'%(i,j,k),((aa+bb)/2,yy,z+3.0),(bb-aa,.38,5.2),'inner',.10)
   for j,(aa,bb) in enumerate(((y0+3,y0+16),(y0+22,y0+34),(y0+40,y1-4))):
    if bb<=aa:continue
    cube(side+'_atrium_glass_%d_%d'%(i,j),(inner,(aa+bb)/2,z+3.5),(.09,bb-aa,4.7),'glass')
    beam(side+'_atrium_sunshade_%d_%d'%(i,j),(inner,aa,z+6.2),(inner,bb,z+6.2),.28,'copper')
   surface(side+'_continuous_canopy_%d'%i,poly,z+7.8,.65,'chalk')
   cube(side+'_social_table_%d'%i,((x0+x1)/2,y1-9,z+1.0),(6,2.2,1.4),'wood',.16)
   if side=='housing':
    cube(side+'_sofa_%d'%i,(x0+9,y0+7,z+.8),(4.7,2,1.3),'cloth',.13)
    vegetation(side+'_inhabited_terrace_%d'%i,x1-7,y1-8,z+.4,.49)
   else:
    vegetation(side+'_research_roofgarden_%d'%i,x0+7,y1-8,z+.4,.51)
   for j,ya in enumerate((y0+7,y0+23,y0+39)):
    if ya+11>y1:continue
    cube(side+'_exterior_daylight_bay_%d_%d'%(i,j),(outer,ya+5,z+3.7),(.10,10,4.5),'glass')
  # The non-repetitive PLEATED STRUCTURAL SKIN visually binds all 4 levels.
  for j,t in enumerate((.08,.30,.67,.90)):
   anchors=[]
   for z,x0,x1,y0,y1 in tiers:
    xx=x0-3.2 if side=='research' else x1+3.2
    anchors.append((xx,y0+(y1-y0)*t,z+3.3))
   for k,(aa,bb) in enumerate(zip(anchors,anchors[1:])):
    beam(side+'_continuous_pleated_rib_%d_%d'%(j,k),aa,bb,1.3,'bronze')
   aa=anchors[0]
   beam(side+'_real_ground_buttress_%d'%j,(aa[0],aa[1]-4,0),aa,1.10,'bronze')
  # Between ribs: asymmetrically spaced large panels, interrupted by glass voids.
  for k in range(len(tiers)-1):
   z,x0,x1,y0,y1=tiers[k];z2,nx0,nx1,ny0,ny1=tiers[k+1]
   ax=x0-3.0 if side=='research' else x1+3.0
   bx=nx0-3.0 if side=='research' else nx1+3.0
   for j,(t0,t1) in enumerate(((.06,.22),(.40,.57),(.78,.93))):
    a0=y0+(y1-y0)*t0;a1=y0+(y1-y0)*t1
    b0=ny0+(ny1-ny0)*t0;b1=ny0+(ny1-ny0)*t1
    ob=surface(side+'_folded_perforated_outer_shell_%d_%d'%(k,j),
        [(ax,a0),(ax,a1),(bx,b1),(bx,b0)],z+4,.35,'copper' if j==1 else 'chalk')
    coords=[(ax,a0,z+4),(ax,a1,z+4),(bx,b1,z2+5),(bx,b0,z2+5)]
    for v,p in zip(ob.data.vertices,coords):v.co=p
    ob.data.update()
 inhabited_bank('research',west)
 inhabited_bank('housing',east)
 # Active public crossing the open negative space. Bridges have real decks,
 # handrail/glazing and primary bearings, not disconnected outlines.
 def occupied_bridge(label,z,y,lo=-17,hi=16,w=6):
  cube(label+'_walkable_deck',((lo+hi)/2,y,z),(hi-lo,w,.75),'limestone',.16)
  for sign in (-1,1):
   yy=y+sign*(w/2-.18)
   beam(label+'_structural_parapet_%d'%sign,(lo,yy,z+.9),(hi,yy,z+.9),.17,'bronze')
   cube(label+'_view_through_guard_%d'%sign,((hi+lo)/2,yy,z+1.2),(hi-lo,.07,1.25),'glass')
  for xx in (lo+2,hi-2):beam(label+'_pier_%d'%int(xx),(xx,y,z-7),(xx,y,z-.4),.66,'bronze')
 occupied_bridge('south_public_court_connection',9.6,17)
 occupied_bridge('shared_garden_research_connection',46,47,-19,15,6.2)
 occupied_bridge('controlled_high_residential_entry',68,61,-19,18,4.0)
 # One compact helix core rather than multiple silhouette-only arch props.
 core=(-2,30);ntreads=235
 for i in range(ntreads):
  angle=2*math.pi*i/51+.2
  z=.35+i*.195;xx=core[0]+6.5*math.cos(angle);yy=core[1]+6.5*math.sin(angle)
  ob=cube('public_spiral_actual_tread_%03d'%i,(xx,yy,z),(2.9,1.15,.23),'chalk',.012)
  ob.rotation_euler.z=angle+math.pi/2
 disk('public_core_vertical_shaft',(core[0],core[1],24.5),1.12,49,'bronze')
 for i,z in enumerate((9.6,26.5,46)):
  cube('helical_landing_at_level_%d'%i,(core[0]-5,core[1]+3,z),(7.2,6.0,.55),'limestone',.16)
 # Varied but coherent crown is integrated with end-floor, not separate shell.
 for prefix,tiers in (('research',west),('housing',east)):
  z,x0,x1,y0,y1=tiers[-1]
  upper=z+13;outer=x0-2 if prefix=='research' else x1+2
  inner=x1 if prefix=='research' else x0
  verts=[(outer,y0-2,z+7.8),(inner,y0+8,z+7.8),
         (inner,y1-9,upper),(outer,y1-4,z+11.6)]
  data=bpy.data.meshes.new('M24_'+prefix+'_crown_fold_mesh')
  data.from_pydata(verts,[],[(0,1,2,3)]);data.update()
  ob=bpy.data.objects.new('M24_'+prefix+'_unique_inhabited_roof_fold',data)
  c.objects.link(ob);ob.data.materials.append(M['chalk']);new.append(ob)
  mod=ob.modifiers.new('Rain_screen_thickness','SOLIDIFY');mod.thickness=.8
  beam(prefix+'_main_crown_truss',verts[0],verts[2],1.2,'bronze')
 # A few deliberate scale figures, NO automatic QA avatars.
 for i,(xx,yy,z) in enumerate(((-6,-20,0),(-11,13,.4),(-30,-8,.4),(26,-41,.4),(-31,39,46.5),(28,41,53.5))):
  disk('scale_person_body_%d'%i,(xx,yy,z+1),.19,1.4,'bronze',10)
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.22,location=(xx,yy,z+1.8))
  o=bpy.context.object;o.name='M24_scale_person_head_%d'%i;link(o)
  o.data.materials.append(M['wood']);new.append(o)
 # Studio lighting: real world, no fake sky backdrop as geometry.
 world=bpy.data.worlds.new('M24_bright_overcast') if scene.world is None else scene.world
 scene.world=world;world.use_nodes=True
 world.node_tree.nodes['Background'].inputs['Color'].default_value=(.66,.75,.78,1)
 world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 def area(name,point,target,power,size):
  data=bpy.data.lights.new('M24_'+name,'AREA');data.energy=power;data.shape='DISK';data.size=size
  o=bpy.data.objects.new('M24_'+name,data);c.objects.link(o);o.location=point
  o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 for name,point,target,power,size in (
  ('east_sun',(80,-70,155),(0,5,25),65000,95),
  ('maker_bounce',(-70,-22,57),(-37,-10,8),15000,43),
  ('housing_daylight',(75,60,130),(31,47,38),45000,65),
  ('research_skylight',(-40,60,115),(-23,40,35),35000,67)):
  area(name,point,target,power,size)
 for name,(eye,target,lens) in CAMERAS.items():
  dat=bpy.data.cameras.new('M24_'+name)
  o=bpy.data.objects.new('M24_CAMERA_'+name,dat);c.objects.link(o)
  o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
  dat.lens=lens
 scene.render.engine='CYCLES';scene.cycles.samples=12
 scene.render.resolution_x=960;scene.render.resolution_y=540
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG'
 scene.view_settings.view_transform='AgX'
 scene['M24']='ART_FIRST_NEW_INHABITED_URBAN_RIDGE_STUDY_NOT_CITY_ADOPTION'
 scene['M24_ART']='HOLD_NOT_APPROVED'
 scene['MINECRAFT_EDUCATION_WRITES']=0
 scene['FORMAL_331_993_AND_G0_S1_G1_G2_G3']='NOT_RUN'
 assert existing_road.name=='M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD'
 assert sha(source())==PIN
 assert len(new)>300,('Insufficient visible architectural components',len(new))
 OUT.mkdir(parents=True)
 blend=OUT/'M24_EDITABLE_SINGLE_INHABITED_HERO.blend'
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for name in CAMERAS:
  scene.camera=bpy.data.objects['M24_CAMERA_'+name]
  png=OUT/('M24_'+name+'.png')
  scene.render.filepath=str(png)
  bpy.ops.render.render(write_still=True)
  assert png.stat().st_size>2000
  views[name]={'sha256':sha(png),'bytes':png.stat().st_size}
 # GLB should only export the new study, not hidden rejected legacy. A copy of
 # the existing M22 road is included for context, not edited or claimed adopted.
 bpy.ops.object.select_all(action='DESELECT')
 for o in new+[existing_road]:
  if o.type=='MESH':o.select_set(True)
 glb=OUT/'M24_INTEGRATED_HERO_ART_HOLD.glb'
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True)
 manifest={'stage':'M24_SINGLE_HERO_ART_FIRST','source_M22_SHA256':PIN,
  'graph_source_sha256':sha(SPEC),'new_meshes':len(new),
  'program':'ONE integrated split-ridge urban landmark / 4 research tiers / 4 residential tiers / 3 sky-bridges / 235 helical prototype treads / sky-open atrium',
  'native_blend_sha256':sha(blend),'glb_sha256':sha(glb),
  'views':views,'actual_creative_direction':'Integrated split-ridge civic landmark with 8 occupied level platforms and central void', 'camera_changed_vs_M23':['research_eye','resident_eye'],'six_M23_view_cameras_frozen':True,
  'not_full_city':True,'not_final_art':True,'art':'HOLD_NOT_APPROVED','adopted':0,
  'minecraft_education':'FORBIDDEN','formal_safety':'NOT_RUN',
  'notice':'Repeated small elements, stair dimensions, and implied rooms are visual study only; not walkability, daylight, structure or code certified'}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
 print('M24_TRUE_NATIVE_SINGLE_HERO_SAVED_ART_HOLD',OUT)
if __name__=='__main__':
 if '--preflight' in sys.argv:print(json.dumps(preflight(),indent=2))
 else:run()
