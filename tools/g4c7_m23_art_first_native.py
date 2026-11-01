#!/usr/bin/env python3
"""M23 ART-FIRST inhabitable civic ridge, using the SHA-pinned M22 native scene.
New architectural study is a distinct editable collection; legacy art stays intact
but render-hidden. No city adoption or Minecraft construction authority.
"""
import hashlib, json, math, os, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/'artifacts/m23_immutable_m22'
SPEC=ROOT/'research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json'
OUT=ROOT/'artifacts/g4c7-m23-art-first-inhabited-urban-ridge'/('run_'+os.getenv('GITHUB_SHA','local')[:12])
PIN='22473a0d17fb59470049fb22b508dcfc294316185d38878b5563e213246af9df'
CAMERAS={
 'south':((9,-155,82),(0,-2,25),38),
 'north':((34,141,100),(-6,8,30),36),
 'oblique':((-152,-96,103),(-4,8,27),36),
 'district':((161,-49,105),(-3,11,31),36),
 'street_eye':((4,-57,2.1),(-8,7,18),28),
 'maker_eye':((-42,-20,2.0),(-23,4,10),23),
 'research_eye':((-28,36,26),(-7,21,32),24),
 'resident_eye':((44,43,33),(8,31,26),22)}
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
 return {'original_M22':str(source()),'M17_nodes':18,'study':'M23_ART_FIRST_UNAPPROVED'}
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
 c=bpy.data.collections.new('M23_NEW_ART_FIRST_INHABITED_CIVIC_RIDGE')
 scene.collection.children.link(c)
 def link(o):
  for prev in list(o.users_collection):prev.objects.unlink(o)
  c.objects.link(o)
  return o
 def mat(name,col,metal=0,rough=.45,glass=0,glow=0):
  m=bpy.data.materials.new('M23_'+name);m.use_nodes=True;m.diffuse_color=(*col,1)
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
  o=bpy.context.object;o.name='M23_'+name;o.dimensions=sz
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
  data=bpy.data.meshes.new('M23_'+name+'_poly')
  data.from_pydata([(x,y,z) for x,y in poly],[],[tuple(range(len(poly)))])
  data.update();ob=bpy.data.objects.new('M23_'+name,data);c.objects.link(ob)
  ob.data.materials.append(M[m]);new.append(ob)
  mod=ob.modifiers.new('Structural_thickness','SOLIDIFY');mod.thickness=thickness
  mod.offset=0
  return ob
 def disk(name,xyz,r,height,m,verts=12):
  bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=height,location=xyz)
  o=bpy.context.object;o.name='M23_'+name;link(o);o.data.materials.append(M[m]);new.append(o);return o
 def vegetation(prefix,x,y,z,scale=1):
  disk(prefix+'_basin',(x,y,z+.6*scale),1.3*scale,.9*scale,'soil')
  disk(prefix+'_trunk',(x,y,z+2.1*scale),.19*scale,3.1*scale,'wood',10)
  for i,(dx,dy,dz,r) in enumerate(((0,0,4.8,2.2),(-1.1,.3,4.1,1.7),(.8,-.6,4.5,1.9))):
   bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=r*scale,
       location=(x+dx*scale,y+dy*scale,z+dz*scale))
   o=bpy.context.object;o.name='M23_'+prefix+'_leaf'+str(i);link(o)
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
 # Public inner garden with visible sky above, never capped by a monolithic shell.
 surface('atrium_room_uncovered',[(-18,-11),(16,-16),(21,32),(-20,34)],.22,.4,'limestone')
 cube('shallow_water_channel',(1.4,8,.49),(4.2,27,.23),'river',.2)
 for i,(x,y) in enumerate(((-10,3),(12,19),(-9,24))):vegetation('court_tree_%02d'%i,x,y,.35,.83)
 # Western maker house: cranked asymmetric industrial wing with real open-front bays.
 # Open front is x toward civic street. Huge roofs are broken into daylight pieces.
 surface('maker_work_floor',[(-62,-30),(-18,-30),(-16,11),(-64,9)],.24,.75,'chalk')
 for i,(x,y) in enumerate(((-50,-17),(-35,-19),(-49,-3),(-31,3))):
  cube('maker_machine_%02d'%i,(x,y,1.15),(6,3.4,2.1),'bronze',.2)
  cube('maker_work_light_%02d'%i,(x,y,2.28),(3,.9,.17),'gold')
  cube('maker_service_island_%02d'%i,(x+3,y+2,.9),(3,1.8,1.7),'wood',.12)
 for i,y in enumerate((-28,-14,1,9)):
  beam('maker_front_column_%d'%i,(-18,y,0),(-18,y,17+i%2*2),.7,'bronze')
 for i,x in enumerate((-62,-48,-34,-18)):
  beam('maker_roof_rib_%d'%i,(x,-29,15.0),(x,8,21.5),.65,'bronze')
 surface('maker_roof_west',[(-64,-29),(-43,-29),(-41,8),(-64,8)],18.8,.75,'copper')
 surface('maker_roof_east',[(-35,-29),(-18,-29),(-18,8),(-34,8)],21.3,.65,'chalk')
 surface('maker_roof_glazed_gap',[(-42,-27),(-36,-27),(-35,6),(-41,6)],20.2,.12,'glass')
 beam('maker_rear_wall_sill',(-61,9,3.1),(-18,9,3.1),.75,'bronze')
 for i,y in enumerate((-22,-7,6)):
  cube('maker_portal_guard_%d'%i,(-19,y,10),(1.0,.28,16),'bronze')
 # Public third-place market: stalls form a lived-in street, not another closed box.
 for i,(x,y,ang) in enumerate(((25,-53,-.10),(37,-38,.18),(23,-24,-.12),(38,-9,.2))):
  cube('market_kiosk_%d'%i,(x,y,1.2),(7,5,2),'wood',.25,rot=ang)
  cube('market_shelter_%d'%i,(x,y,4.2),(11,7,.28),'cloth',.09,rot=ang)
  for s in (-1,1):beam('kiosk_post_%d_%d'%(i,s),(x+s*4,y-2.4,0),(x+s*4,y-2.4,4.1),.22,'bronze')
 # North research ridge: multi-level buildings physically enclosing inhabitable floors,
 # with vertical separation and an open glazed face to public atrium.
 for i,(z,x0,x1,y0,y1) in enumerate(((9.6,-47,-8,14,59),
  (20,-52,-11,22,65),(30.4,-49,-9,30,71),(42,-43,-12,38,74),(55,-38,-16,45,78))):
  poly=[(x0,y0),(x1,y0-2),(x1+2,y1),(x0-3,y1-3)]
  surface('research_inhabited_floor_%d'%i,poly,z,.65,'chalk')
  # Research labs have deep slabs, actual sheltered work rooms, not an empty high silhouette.
  cube('research_inner_room_%d'%i,((x0+x1)*.5,(y0+y1)*.5,z+2.2),
       ((x1-x0)-6,(y1-y0)*.45,4.0),'inner',.25)
  for j,x in enumerate((x0+6,x0+15,x0+24)):
   if x<x1-2:
    cube('research_natural_light_window_%d_%d'%(i,j),(x,y0+.2,z+3.2),(6,.13,3.8),'glass')
    cube('research_mullion_%d_%d'%(i,j),(x+3.15,y0+.15,z+3.2),(.24,.3,4),'bronze')
  surface('research_living_roof_%d'%i,
    [(x0,y0),(x1,y0-2),(x1+2,y0+11),(x0-3,y0+10)],z+7.2,.48,
    'copper' if i%2 else 'chalk')
  if i in (1,3):vegetation('research_sky_court_%d'%i,x0+5,y1-8,z+.4,.7)
  for y in (y0+2,y1-4):beam('research_load_buttress_%d_%d'%(i,int(y)),(x0+1,y,z-.4),(x0+6,y+2,z+7.5),.58,'bronze')
  # Visible occupied desks toward public edge
  for j in range(3):
   x=x0+8+j*8
   if x<x1-3:
    cube('research_workbench_%d_%d'%(i,j),(x,y0+7,z+.95),(3.2,1.5,1.3),'wood',.1)
  if i:
   beam('research_continuous_core_%d'%i,(-35,48,z-11.0),(-35,48,z+1.4),2,'bronze')
 # Distinct east residential ridge: 12 actual rooms at multiple staggered levels,
 # each with floor, balcony, glazing, openings, desk and private planting.
 level_heights=[9.6,21,34,47,61,75]
 for i,z in enumerate(level_heights):
  for j in range(2):
   x=27 + j*18 + (i%3-1)*4
   y=22 + i*8 + (j*10 if i%2 else -j*5)
   yaw=math.radians((i%4-1.5)*7 + (j*2-1)*6)
   w=14.0 if j==0 else 13.0;d=11.5
   # room boundaries leave large front glazed aperture
   cube('residence_floor_%d_%d'%(i,j),(x,y,z),(w,d,.6),'chalk',.3,rot=yaw)
   cube('residence_back_wall_%d_%d'%(i,j),(x,y+d*.48,z+3.0),(w,.52,5.8),'inner',.1,rot=yaw)
   for side in (-1,1):
    cube('residence_side_fin_%d_%d_%d'%(i,j,side),(x+side*(w/2-.25),y,z+3.3),(.55,d,6.5),'bronze',.1,rot=yaw)
   cube('residence_glass_bay_%d_%d'%(i,j),(x,y-d*.46,z+3.2),(w-1.3,.16,5.25),'glass',.02,rot=yaw)
   cube('residence_roof_%d_%d'%(i,j),(x,y,z+6.55),(w+.9,d+.4,.7),'limestone',.23,rot=yaw)
   cube('residence_balcony_%d_%d'%(i,j),(x,y-d*.68,z+.03),(w*.78,4.0,.43),'copper',.15,rot=yaw)
   cube('residence_desk_%d_%d'%(i,j),(x+1.2,y,z+1.1),(2.6,1.5,1.4),'wood',.15,rot=yaw)
   cube('residence_sofa_%d_%d'%(i,j),(x-2.7,y+1.9,z+.6),(3.6,1.5,1.0),'cloth',.16,rot=yaw)
   disk('residence_planter_%d_%d'%(i,j),(x+4,y-4.3,z+.67),.8,1,'soil',12)
   if (i+j)%3==0:vegetation('home_terrace_tree_%d_%d'%(i,j),x+4.3,y-6,z+.2,.43)
 # Visible inclined ties link building ridges to civic street at height.
 for i,z in enumerate((12,24,37,50,64)):
  beam('housing_primary_diagrid_A_%d'%i,(16,16+i*5,max(z-12,0)),(35,30+i*6,z),.65,'bronze')
  beam('housing_primary_diagrid_B_%d'%i,(57,16+i*5,max(z-11,0)),(31,32+i*6,z+4),.7,'bronze')
 # Physical public second street: destination points from M17, not free-floating sculpture.
 nodes={n['id']:n['xyz'] for n in json.loads(SPEC.read_text())['nodes']}
 def bridge(name,a,b,z,w=5):
  ax,ay=nodes[a][:2];bx,by=nodes[b][:2]
  dx=bx-ax;dy=by-ay;L=math.hypot(dx,dy)
  o=cube(name+'_occupied_deck',((ax+bx)*.5,(ay+by)*.5,z),(L,w,.55),'chalk',.12,rot=math.atan2(dy,dx))
  perp=(-dy/L,dx/L)
  for side in (-1,1):
   aa=(ax+perp[0]*w*.48*side,ay+perp[1]*w*.48*side,z+1.1)
   bb=(bx+perp[0]*w*.48*side,by+perp[1]*w*.48*side,z+1.1)
   beam(name+'_parapet_%d'%side,aa,bb,.16,'bronze')
 bridge('maker_to_research_skywalk','U0_SOUTH_GALLERY','U1_RESEARCH_OBSERVATORY',9.6)
 bridge('research_to_garden_skywalk','U1_RESEARCH_OBSERVATORY','U2_SKY_GARDEN',9.6)
 bridge('garden_to_north_skywalk','U2_SKY_GARDEN','U3_NORTH_GALLERY',9.6)
 stair('south_public_stair',(-19,-17),(-24,13),0,9.6,4.2,48)
 stair('north_public_stair',(23,56),(7,31),0,9.6,4.2,48)
 cube('roof_garden_public_occupied_floor',(3,38,9.6),(25,20,.6),'chalk',.2)
 for i,(x,y) in enumerate(((0,35),(9,44),(-5,44))):vegetation('public_skygarden_%d'%i,x,y,9.8,.6)
 # Three separated dramatic exoskeleton portals, rooted in lived maker/research/housing.
 # NOT a continuous shell enclosing the city.
 for k,(yy,height) in enumerate(((-12,35),(16,51),(43,65))):
  coords=[]
  for i in range(21):
   t=i/20;x=-63+125*t
   zz=7+height*math.sin(math.pi*t)**.86
   coords.append((x,yy+4*math.sin(t*math.pi),zz))
  for i,(a,b) in enumerate(zip(coords,coords[1:])):
   beam('open_air_civic_portal_%d_%02d'%(k,i),a,b,.78,'bronze')
  for j,xi in enumerate((1,6,11,16,19)):
   x,y,z=coords[xi]
   if z>20:beam('portal_louver_%d_%d'%(k,j),(x,y,z),
       (x+2,y+8,z-4),'copper')
 # Inhabited human scale: visibly living/walking users not official QA avatars.
 for i,(x,y,z) in enumerate(((-13,-23,0),(-2,3,.25),(7,23,.25),(-28,-14,.5),
                              (24,-45,0),(-27,29,10.2),(3,36,10.2),(43,39,34.4))):
  disk('visual_scale_human_body_%d'%i,(x,y,z+.9),.2,1.45,'bronze',10)
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.24,location=(x,y,z+1.72))
  o=bpy.context.object;o.name='M23_visual_scale_human_head_%d'%i;link(o)
  o.data.materials.append(M['wood']);new.append(o)
 # Studio lighting: real world, no fake sky backdrop as geometry.
 world=bpy.data.worlds.new('M23_bright_overcast') if scene.world is None else scene.world
 scene.world=world;world.use_nodes=True
 world.node_tree.nodes['Background'].inputs['Color'].default_value=(.66,.75,.78,1)
 world.node_tree.nodes['Background'].inputs['Strength'].default_value=.8
 def area(name,point,target,power,size):
  data=bpy.data.lights.new('M23_'+name,'AREA');data.energy=power;data.shape='DISK';data.size=size
  o=bpy.data.objects.new('M23_'+name,data);c.objects.link(o);o.location=point
  o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 for name,point,target,power,size in (
  ('east_sun',(80,-70,155),(0,5,25),65000,95),
  ('maker_bounce',(-70,-22,57),(-37,-10,8),15000,43),
  ('housing_daylight',(75,60,130),(31,47,38),45000,65),
  ('research_skylight',(-40,60,115),(-23,40,35),35000,67)):
  area(name,point,target,power,size)
 for name,(eye,target,lens) in CAMERAS.items():
  dat=bpy.data.cameras.new('M23_'+name)
  o=bpy.data.objects.new('M23_CAMERA_'+name,dat);c.objects.link(o)
  o.location=eye;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
  dat.lens=lens
 scene.render.engine='CYCLES';scene.cycles.samples=12
 scene.render.resolution_x=960;scene.render.resolution_y=540
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG'
 scene.view_settings.view_transform='AgX'
 scene['M23']='ART_FIRST_NEW_INHABITED_URBAN_RIDGE_STUDY_NOT_CITY_ADOPTION'
 scene['M23_ART']='HOLD_NOT_APPROVED'
 scene['MINECRAFT_EDUCATION_WRITES']=0
 scene['FORMAL_331_993_AND_G0_S1_G1_G2_G3']='NOT_RUN'
 assert existing_road.name=='M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD'
 assert sha(source())==PIN
 assert len(new)>275,('Insufficient visible architectural components',len(new))
 OUT.mkdir(parents=True)
 blend=OUT/'M23_EDITABLE_CIVIC_RIDGE_ART_STUDY.blend'
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for name in CAMERAS:
  scene.camera=bpy.data.objects['M23_CAMERA_'+name]
  png=OUT/('M23_'+name+'.png')
  scene.render.filepath=str(png)
  bpy.ops.render.render(write_still=True)
  assert png.stat().st_size>2000
  views[name]={'sha256':sha(png),'bytes':png.stat().st_size}
 # GLB should only export the new study, not hidden rejected legacy. A copy of
 # the existing M22 road is included for context, not edited or claimed adopted.
 bpy.ops.object.select_all(action='DESELECT')
 for o in new+[existing_road]:
  if o.type=='MESH':o.select_set(True)
 glb=OUT/'M23_NEW_ARCHITECTURE_NOT_ADOPTED.glb'
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True)
 manifest={'stage':'M23_ART_FIRST','source_M22_SHA256':PIN,
  'graph_source_sha256':sha(SPEC),'new_meshes':len(new),
  'program':'Maker work-floor / market / exposed courtyard / 5 research tiers / 12 habitable rooms / public skywalks / 96 actual stair treads',
  'native_blend_sha256':sha(blend),'glb_sha256':sha(glb),
  'views':views,'actual_creative_direction':'Three open civic portals with distinct maker, research and residential inhabited masses',
  'not_full_city':True,'not_final_art':True,'art':'HOLD_NOT_APPROVED','adopted':0,
  'minecraft_education':'FORBIDDEN','formal_safety':'NOT_RUN',
  'notice':'Repeated small elements, stair dimensions, and implied rooms are visual study only; not walkability, daylight, structure or code certified'}
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
 print('M23_REAL_3D_ART_FIRST_CIVIC_RIDGE_SAVED_NOT_APPROVED',OUT)
if __name__=='__main__':
 if '--preflight' in sys.argv:print(json.dumps(preflight(),indent=2))
 else:run()
