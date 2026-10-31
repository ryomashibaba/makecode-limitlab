#!/usr/bin/env python3
"""D3S26 M12 - authored inhabited city silhouette, one visual-first hypothesis.
Native Blender evidence only. NOT an ART PASS, route QA, or construction permission.
"""
from pathlib import Path
import hashlib, json, math, os, sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts/g4c7-d3s26-m12-visual-first"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
# Each ring is an intentional section of a different occupied district.
# These are NOT one repeated tower specification.
DISTRICTS=[
 {"name":"NORTH_RESEARCH","use":"research","heights":[0,33,78,126,174,216],
  "rings":[(-98,55,1.00),(-104,47,1.21),(-89,53,.95),(-73,69,1.05),(-86,75,.70),(-99,70,.32)],
  "shape":[(-37,-31),(-6,-42),(30,-23),(37,7),(7,37),(-26,31)],
  "mouth":0,"material":"stone"},
 {"name":"EAST_RESIDENCE","use":"residential","heights":[0,26,58,111,153,189],
  "rings":[(107,85,1.00),(99,77,1.12),(116,72,.86),(120,97,1.09),(109,99,.67),(105,89,.26)],
  "shape":[(-31,-22),(9,-36),(36,-5),(30,30),(-8,41),(-38,8)],
  "mouth":0,"material":"warm"},
 {"name":"MID_CULTURE","use":"culture","heights":[0,17,54,92,131],
  "rings":[(-7,109,1.00),(-20,102,1.18),(-6,108,.86),(12,94,.80),(1,108,.35)],
  "shape":[(-34,-18),(8,-39),(39,-10),(32,22),(-13,39),(-38,12)],
  "mouth":0,"material":"copper"},
 {"name":"SOUTH_MAKER","use":"maker","heights":[0,16,39,72,96],
  "rings":[(48,-86,1.00),(51,-79,1.22),(61,-74,1.00),(75,-69,.77),(79,-62,.43)],
  "shape":[(-48,-24),(-10,-40),(40,-28),(48,5),(15,32),(-42,23)],
  "mouth":0,"material":"stone"},
 {"name":"WEST_MARKET","use":"market","heights":[0,11,29,45,63],
  "rings":[(-124,-93,1.00),(-132,-85,1.19),(-116,-72,.78),(-108,-68,.91),(-120,-63,.41)],
  "shape":[(-33,-17),(2,-33),(31,-6),(22,22),(-13,32),(-35,7)],
  "mouth":0,"material":"copper"}]
CAMERAS={
"south":((0,-395,240),(0,15,100)),
"north":((0,385,260),(0,12,96)),
"oblique":((-315,-302,265),(0,8,112)),
"district":((302,-240,230),(0,30,110)),
"street_eye":((-69,-19,1.7),(20,38,28)),
"maker_eye":((37,-104,1.7),(58,-80,8)),
"research_eye":((-49,10,42),(23,29,50)),
"resident_eye":((66,45,75),(10,16,83))}
def preflight():
 assert len(DISTRICTS)==5 and len(CAMERAS)==8
 for d in DISTRICTS:
  assert len(d['heights'])==len(d['rings']) and len(d['shape'])>=5
  assert all(b>a for a,b in zip(d['heights'],d['heights'][1:]))
  assert len(set(tuple(x) for x in d['shape']))==len(d['shape'])
 return {'stage':'D3S26_M12','art':'HOLD','safety':'NOT_RUN','minecraft':'FORBIDDEN',
         'integration':'FORBIDDEN','interpretation':'ONE_VISUAL_MEDIUM_STUDY_NOT_CITY'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def author():
 import bpy
 from mathutils import Vector
 info=preflight()
 assert not OUT.exists(),"Append-only evidence destination already exists"
 OUT.mkdir(parents=True)
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 scene=bpy.context.scene
 def material(name,rgba,metal=0,rough=.48,emit=0):
  m=bpy.data.materials.new(name);m.use_nodes=True
  p=m.node_tree.nodes.get('Principled BSDF')
  p.inputs['Base Color'].default_value=(*rgba,1)
  p.inputs['Metallic'].default_value=metal
  p.inputs['Roughness'].default_value=rough
  if emit:
   p.inputs['Emission Color'].default_value=(*rgba,1)
   p.inputs['Emission Strength'].default_value=emit
  return m
 MAT={
 "stone":material("M12 mineral porcelain",(.56,.67,.68),.24),
 "warm":material("M12 warm inhabited ceramic",(.71,.62,.51),.12),
 "copper":material("M12 muted copper oxide",(.53,.36,.27),.40),
 "glass":material("M12 deep cyan structural glazing",(.10,.28,.34),.33,.24),
 "floor":material("M12 paved interior floors",(.27,.37,.38)),
 "garden":material("M12 living garden",(.12,.33,.23)),
 "light":material("M12 city illumination",(.95,.70,.42),.0,.45,.18),
 "street":material("M12 stone city floor",(.36,.40,.39)),
 }
 C={}
 for name in ("01_INHABITED_DISTRICTS","02_TRUE_PUBLIC_GROUND","03_HUMAN_ACTIVITY","04_REVIEW_CAMERAS_LIGHT"):
  coll=bpy.data.collections.new(name);scene.collection.children.link(coll);C[name]=coll
 def obj(name,v,faces,mat,coll="01_INHABITED_DISTRICTS"):
  mesh=bpy.data.meshes.new(name+"_data")
  mesh.from_pydata(v,[],faces);mesh.update()
  ob=bpy.data.objects.new(name,mesh);C[coll].objects.link(ob)
  mesh.materials.append(MAT[mat])
  return ob
 def box(name,center,size,mat,coll="03_HUMAN_ACTIVITY"):
  x,y,z=center;w,h,d=[k/2 for k in size]
  v=[(x+u*w,y+q*h,z+r*d) for r in (-1,1) for q in (-1,1) for u in (-1,1)]
  faces=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(1,5,7,3),(3,7,6,2),(2,6,4,0)]
  return obj(name,v,faces,mat,coll)
 def quad(name,p,mat,thick=.3,coll="01_INHABITED_DISTRICTS"):
  ob=obj(name,p,[(0,1,2,3)],mat,coll)
  if thick:
   mod=ob.modifiers.new("RealEditThickness","SOLIDIFY");mod.thickness=thick
  return ob
 def ring(d,i):
  x,y,s=d['rings'][i];return [(x+u*s,y+v*s,d['heights'][i]) for u,v in d['shape']]
 for d in DISTRICTS:
  key=d['name'];n=len(d['shape']);R=[ring(d,j) for j in range(len(d['rings']))]
  # Individual edited silhouette facets - no auto floors or repeated storeys.
  for level in range(len(R)-1):
   for k in range(n):
    a,b=R[level][k],R[level][(k+1)%n]
    c,e=R[level+1][(k+1)%n],R[level+1][k]
    material_name='glass' if ((level*3+k)%7 in (1,3)) else d['material']
    if level==0 and k==d['mouth']:
     def inter(p,q,t):return tuple(p[m]*(1-t)+q[m]*t for m in range(3))
     topa=inter(a,e,.35);topb=inter(b,c,.35)
     for part,ua,ub,vc,vd in [
        ('L',a,inter(a,b,.26),inter(topa,topb,.26),topa),
        ('R',inter(a,b,.74),b,topb,inter(topa,topb,.74)),
        ('TOP',topa,topb,c,e)]:
      quad(key+'_TRUE_ENTRY_'+part,[ua,ub,vc,vd],d['material'],.65)
    else:
     quad(key+'_FACADE_%02d_%02d'%(level,k),[a,b,c,e],material_name,.65)
  obj(key+"_SKY_EDGE",R[-1],[tuple(range(n))],d['material'])
  # Ground slab inside the architectural footprint is real, not a colored label.
  obj(key+'_INHABITED_GROUND',[(x,y,-.25) for x,y,z in R[0]],[tuple(range(n))],'floor')
  # Real occupied midlevel landing with deliberate open section in the roof.
  idx=1 if len(R)>3 else 0
  ob=obj(key+'_MIDLEVEL_GALLERY',[(x,y,d['heights'][idx]-.35) for x,y,_ in R[idx]],
         [tuple(range(n))],'floor')
  # Real task object, eye/route are not yet formally certified.
  center=d['rings'][0];box(key+'_OCCUPIED_SERVICE_WORKTOP',
      (center[0],center[1],1.1),(5,3.2,2.2),'light')
 # Winding public ground, authored coordinates with real width.
 path=[(-165,-138),(-128,-124),(-78,-112),(-35,-80),(5,-42),(37,-12),(71,18),(100,44)]
 widths=[13,18,22,20,23,25,17,13]
 left=[];right=[]
 for i,(x,y) in enumerate(path):
  before=path[max(0,i-1)];after=path[min(len(path)-1,i+1)]
  dx,dy=after[0]-before[0],after[1]-before[1]
  m=math.hypot(dx,dy)
  nx,ny=-dy/m,dx/m
  left.append((x+nx*widths[i],y+ny*widths[i],.04))
  right.append((x-nx*widths[i],y-ny*widths[i],.04))
 for i in range(len(path)-1):
  quad("M12_TRUE_CIVIC_GROUND_%02d"%i,
      [left[i],right[i],right[i+1],left[i+1]],'street',.6,"02_TRUE_PUBLIC_GROUND")
 # Exposed fabrication hall, visited streetfront and upper observation terraces.
 box("M12_MAKER_BENCH_EXPLICIT",(42,-76,2.5),(15,8,5),'light')
 box("M12_CIVIC_GALLERY_TRUE_FLOOR",(-10,-4,23),(36,15,1),'floor')
 box("M12_CIVIC_GARDEN_TRUE_FLOOR",(63,24,44),(31,19,1),'garden')
 box("M12_DISTRICT_FOOTBRIDGE",(14,12,31),(28,11,1.1),'stone')
 # Deliberately sparse human-scale trees; not proxy for architecture.
 for i,(x,y) in enumerate([(-46,-42),(-19,-24),(14,-4),(35,12),(91,30)]):
  box("M12_TREE_TRUNK_%02d"%i,(x,y,2.5),(1.0,1.0,5),'copper')
  box("M12_TREE_CROWN_%02d"%i,(x,y,6.2),(6.5,6.5,3.0),'garden')
 # Unambiguous world, no background "skyline" image.
 scene.world.color=(.47,.57,.63)
 scene.render.engine='CYCLES';scene.cycles.samples=12
 scene.render.resolution_x=960;scene.render.resolution_y=540
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG'
 scene.view_settings.view_transform='AgX'
 def sun(name,loc,strength,size):
  data=bpy.data.lights.new(name,'AREA');data.energy=strength;data.shape='DISK';data.size=size
  ob=bpy.data.objects.new(name,data);C["04_REVIEW_CAMERAS_LIGHT"].objects.link(ob)
  ob.location=loc;ob.rotation_euler=(Vector((0,0,30))-ob.location).to_track_quat('-Z','Y').to_euler()
 for t in [('Dawn',(25,-100,330),65000,240),('Skyfill',(-130,110,250),38000,230)]:
  sun(*t)
 for name,(loc,target) in CAMERAS.items():
  cam=bpy.data.cameras.new('M12_CAM_'+name)
  ob=bpy.data.objects.new('M12_CAM_'+name,cam);C["04_REVIEW_CAMERAS_LIGHT"].objects.link(ob)
  ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
  cam.lens=32 if 'eye' in name else 38
 scene['G4C7_ART']='HOLD_NOT_APPROVED'
 scene['MINECRAFT_EDUCATION_CONSTRUCTION']='FORBIDDEN'
 scene['G0_S1_G1_G2_G3']='NOT_RUN'
 scene['ART_DIRECTION']='Manual city silhouette cross-sections, not generator-driven repeated boxes'
 blend=OUT/'M12_HAND_AUTHORED_DISTRICT_SCENE.blend'
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for key in CAMERAS:
  scene.camera=bpy.data.objects['M12_CAM_'+key]
  png=OUT/('M12_'+key+'.png');scene.render.filepath=str(png)
  bpy.ops.render.render(write_still=True)
  assert png.stat().st_size>2048
  views[key]={'bytes':png.stat().st_size,'sha256':sha(png)}
 bpy.ops.object.select_all(action='DESELECT')
 for o in bpy.data.objects:
  if o.type=='MESH' and not o.hide_render:o.select_set(True)
 glb=OUT/'M12_REAL_MESH_UNASSESSED.glb'
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True)
 m={'input':'authored cross sections','stage':'M12','art':'HOLD',
    'construction':'FORBIDDEN','formal_QA':'NOT_RUN',
    'blender':bpy.app.version_string,'blend_sha256':sha(blend),
    'glb_sha256':sha(glb),'views':views,'district_count':len(DISTRICTS),
    'size_warning':'model units not Minecraft blocks; not construction-ready'}
 (OUT/'manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
 print('M12_NATIVE_EVIDENCE_WRITTEN_ART_UNASSESSED',OUT)
if __name__=='__main__':
 if '--preflight' in sys.argv:print(json.dumps(preflight()))
 else:author()
