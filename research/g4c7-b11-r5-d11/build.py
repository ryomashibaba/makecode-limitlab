"""G4-C7 B11-R5 D11 experimental *local* inhabited folded canyon.
Author-controlled spatial program, NOT art-adopted, NOT certified, NOT Minecraft output.
Same physical model exports OBJ/GLB/per-role PLY for independent rendering and audit.
"""
from pathlib import Path
import json, hashlib, argparse, math
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
COLOR={
 'terrain':(43,60,71,255),'fault_mass':(116,135,149,255),
 'ceramic':(191,198,189,255),'dark_skin':(53,75,90,255),
 'public':(229,187,110,255),'maker':(228,125,91,255),
 'research':(97,177,205,255),'habitat':(164,200,151,255),
 'garden':(75,159,120,255),'structural':(101,143,164,255),
 'glass':(101,207,225,160),'core':(68,167,181,255),
 'light':(247,215,140,255),
}
items={}; program=[]

def add(m,k,label=''):
 assert np.isfinite(m.vertices).all() and len(m.faces)>0
 m.visual.vertex_colors=np.tile(COLOR[k],(len(m.vertices),1))
 items[k].append(m)
 if label: program.append({'role':k,'label':label,'center':m.bounds.mean(axis=0).round(2).tolist()})

def box(cx,cy,cz,sx,sy,sz,cat,label=''):
 assert min(sx,sy,sz)>0
 m=trimesh.creation.box(extents=[sx,sy,sz]);m.apply_translation([cx,cy,cz]);add(m,cat,label)

def rod(a,b,r,cat,label=''):
 m=trimesh.creation.cylinder(radius=r,segment=[a,b],sections=10);add(m,cat,label)

def polyloft(a,b,z0,z1,cat,label=''):
 """Between two ordered convex polygon sections; physical polygon faces, not schematic lines."""
 a=np.asarray(a,float);b=np.asarray(b,float);n=len(a)
 assert a.shape==b.shape and n>=3 and z1>z0
 verts=np.vstack([np.column_stack([a,np.full(n,z0)]),np.column_stack([b,np.full(n,z1)])]);faces=[]
 for i in range(1,n-1):faces.extend([(0,i+1,i),(n,n+i,n+i+1)])
 for i in range(n):j=(i+1)%n;faces.extend([(i,j,n+j),(i,n+j,n+i)])
 m=trimesh.Trimesh(vertices=verts,faces=faces,process=False)
 add(m,cat,label)

def ribbon(pts,width,cat,depth=1.5,label=''):
 ps=np.asarray(pts,float)
 assert len(ps)>=2
 for i,(a,b) in enumerate(zip(ps[:-1],ps[1:])):
  v=b-a;h=np.linalg.norm(v[:2]);assert h>1e-4
  u=np.array([-v[1],v[0],0])/h*width/2
  top=np.array([a-u,a+u,b+u,b-u]);lower=top-np.array([0,0,depth]);verts=np.vstack([top,lower]);fs=[(0,1,2),(0,2,3),(4,6,5),(4,7,6)]
  for j in range(4):k=(j+1)%4;fs.extend([(j,k,k+4),(j,k+4,j+4)])
  add(trimesh.Trimesh(vertices=verts,faces=fs,process=False),cat,label if i==0 else '')

def plate(points,zlo,zhi,cat,label=''):
 polyloft(points,points,zlo,zhi,cat,label)

def terrace(axis, side, z, scale,cat,index):
 """Layered inhabited *deep rooms* facing central canyon; widths are nonrepeating."""
 if side=='west':
  y=axis
  # U-shaped room, anchored west in massive wall; transparent facing east
  x=-239+index*5
  width=65+index*7
  box(x,y,z-5,width,38+index*3,10,cat,'inhabited room volume west')
  box(x+width/2-2,y,z+4,3,37+index*3,13,'glass','canyon-facing occupied frontage')
  box(x+width/2+8,y,z-4,19,32,2,'public','overlook terrace')
 else:
  x=239-index*6
  width=60+index*7
  box(x,axis,z-5,width,35+index*3,10,cat,'research/residence deep volume east')
  box(x-width/2+2,axis,z+4,3,34+index*3,13,'glass','canyon-facing occupied frontage')
  box(x-width/2-8,axis,z-4,19,32,2,'public','overlook terrace')

def west_fold():
 # Not a filled megawall: oblique, separately rooted long inhabited escarpment
 low=np.array([[-305,-180],[-257,-229],[-201,-200],[-218,180],[-280,226],[-328,177]])
 mid=np.array([[-324,-131],[-279,-203],[-222,-187],[-215,205],[-274,262],[-353,205]])
 top=np.array([[-354,-82],[-300,-171],[-246,-148],[-233,245],[-318,294],[-382,225]])
 polyloft(low,mid,7,111,'fault_mass','western asymmetric maker escarpment')
 polyloft(mid,top,111,238,'ceramic','western lifted inhabited terrain')
 # angular negative sections cut by arranging open frontage, varied terraces in canyon
 for i,(y,z) in enumerate([(-145,47),(-75,93),(15,139),(103,189)]):
  terrace(y,'west',z,1,'maker' if i<2 else 'habitat',i)
 # front structural facets angled into the support footprint, none spans central view
 for a,b in [((-294,-170,16),(-267,-110,150)),((-315,130,10),(-250,91,185))]:rod(a,b,5,'structural')
 # roof terraces are wider where external habitat exists, staggered
 plate([[-359,-43],[-288,-65],[-260,50],[-336,88]],237,241,'garden','inhabited sky garden')

def east_fold(active=True):
 if not active:
  # Minimal public access core remains for failure attribution, but research and shaping removed
  return
 low=np.array([[215,-204],[267,-214],[320,-172],[334,132],[279,207],[205,171]])
 mid=np.array([[237,-183],[298,-215],[362,-141],[350,162],[301,239],[222,173]])
 top=np.array([[239,-155],[345,-178],[406,-110],[367,197],[299,268],[224,188]])
 polyloft(low,mid,7,115,'fault_mass','east science-public escarpment')
 polyloft(mid,top,115,256,'ceramic','east civic highland')
 for i,(y,z) in enumerate([(-143,54),(-54,109),(40,154),(129,211)]):
  terrace(y,'east',z,1,'research' if i<3 else 'habitat',i)
 plate([[243,202],[297,223],[360,178],[326,262]],254,259,'garden','research roof garden')
 for a,b in [((275,-140,7),(294,-99,147)),((303,145,7),(259,125,202))]:rod(a,b,5,'structural')

def inhabited_fault_core(h=70,research=True):
 # Ground-level public courtyard is open to sky. Outer open relationship rather than third monolith.
 box(0,-24,9,725,530,18,'terrain','ground occupied urban canyon section')
 # Original asymmetric fault edges produce human-scaled civic slivers
 west_fold(); east_fold(research)
 # Manufacture floor bounded by high roof in west, public entrance across the plaza
 box(-118,44,19,133,115,2,'maker','publicly observable active fabrication floor')
 box(-143,39,23,37,28,6,'maker','large manufactured object')
 box(-100,50,33,30,22,21,'maker','suspended workshop object')
 # Working roof is a spatial large-span internal need. Angled shelter anchored partly in west cliff.
 # Visibly covers maker zone, rather than becoming rectangular megaslab spanning whole city.
 low=[[-207,-15],[-190,-48],[-48,-39],[-20,26],[-51,114],[-193,120]]
 high=[[-220,-3],[-196,-65],[-54,-54],[-17,33],[-64,122],[-206,138]]
 roof_soffit=20+h
 polyloft(low,high,roof_soffit,roof_soffit+10,'dark_skin','maker covered free-height zone')
 # East research sees public experiment from same public ground level, not exclusively sky floor
 if research:
  box(122,61,20,109,107,3,'research','visible live civic research floor')
  for x,y,z in [(91,48,24),(132,73,26),(153,34,24)]:
   box(x,y,z,13,12,6,'research','public science experiment station')
  box(153,134,139,114,51,8,'research','upper public research learning rooms')
  box(110,107,133,62,22,2,'public','upper research balcony')
  box(159,119,145,61,1.7,12,'glass','science canyon full opening')
 # Main ground route is separated from production and science floors by distinct frontage
 route=[[-281,-93,20],[-234,-91,20],[-166,-92,20],[-91,-95,20],[-17,-94,20],[50,-92,20],[126,-89,20],[192,-87,20],[250,-81,20],[285,-41,20],[294,45,20]]
 ribbon(route,11,'public',1.5,'actual shared promenade')
 # Two separate lobbies and real geometries at 20, 132 and 220; NOT functioning lifts
 for name,x,y in [('E1',-285,55),('E2',283,55)]:
  box(x,y,20,23,26,2,'core',name+' ground lobby slab')
  box(x,y,132,23,26,2,'core',name+' research landing slab')
  box(x,y,220,23,26,2,'core',name+' sky landing slab')
  for dx,dy in [(-9,-10),(-9,10),(9,-10),(9,10)]:
   rod((x+dx,y+dy,16),(x+dx,y+dy,226),1.3,'core')
  # Solid footprint connection to common ground route, not 3D traversability proof
  ribbon([(x,-88,20),(x,-30,20),(x,22,20),(x,55,20)],8,'public',1.4,name+' street-to-lobby')
 # Curved public research bridge/floor physically reaches the two z132 lobbies
 upper=[(-285,55,132),(-216,86,132),(-138,124,132),(-45,146,132),
        (45,144,132),(119,127,132),(199,89,132),(283,55,132)]
 ribbon(upper,10,'public',2.2,'public research level connects both core landings')
 if research:ribbon([(119,127,132),(145,129,132),(153,134,132)],8,'public',2,'upper research entry bridge')
 # Sky civic: not a disconnected mega plate; directly joins two landings, gated residence branches.
 high=[(-285,55,220),(-214,125,220),(-122,161,220),(-22,158,220),(80,159,220),(184,118,220),(283,55,220)]
 ribbon(high,9,'public',2.2,'upper sky boulevard connected to both cores')
 for x,y in [(-190,165),(-95,202),(4,211),(108,206),(190,164)]:
  box(x,y,219,55,24,6,'habitat','upper inhabited neighborhood facing canyon')
  box(x,y-14,227,47,3.8,10,'glass','dwelling daylight frontage')
  box(x,y-26,219,35,16,2,'garden','semi-private planted threshold')
  # explicit conceptual private threshold, not a safe door
  rod((x,y-30,219),(x,y-30,229),.55,'structural')
 # 3 long section floor beams deep-laminated and inclined, infrequent (not D7 spines)
 for a,b in [((-310,-170,9),(-250,-115,186)),((314,-181,10),(285,-109,203))]:rod(a,b,6,'structural','ground rooted edge support hypothesis')
 # canopy of pointed urban wedge with a large open civic void; no central mass above sky
 for x,y in [(-89,-65),(80,-71),(190,-28)]:
  box(x,y,18,45,29,4,'public','public assembly pocket')
  rod((x,y,20),(x,y,22),.18,'light')
 return route

def build(h=70,research=True):
 assert h in (70,90)
 global items,program
 items={k:[] for k in COLOR};program=[]
 route=inhabited_fault_core(h,research)
 folder=ROOT/(('full' if research else 'without_research')+'_'+str(h));folder.mkdir(parents=True,exist_ok=True)
 scene=trimesh.Scene();big=[];meta={}
 for tag,mesh in items.items():
  if not mesh:continue
  m=trimesh.util.concatenate(mesh); m.export(folder/f'{tag}.ply');scene.add_geometry(m,geom_name=tag);big.append(m)
  meta[tag]={'faces':len(m.faces),'sha256_ply':hashlib.sha256((folder/f'{tag}.ply').read_bytes()).hexdigest()}
 full=trimesh.util.concatenate(big);full.export(folder/'study.obj');scene.export(folder/'study.glb')
 manifest={'stage':'G4-C7 B11-R5 D11','scope':'LOCAL 725x530m inhabitance study; NOT citywide or final model',
   'case':h,'research_present':research,'roof_soffit_target_z_m':20+h,
   'maker_floor_target_z_m':20,'route_points':route,'faces':len(full.faces),
   'bounds_m':full.bounds.tolist(),'sha256_obj':hashlib.sha256((folder/'study.obj').read_bytes()).hexdigest(),
   'sha256_glb':hashlib.sha256((folder/'study.glb').read_bytes()).hexdigest(),
   'categories':meta,'program_count':len(program),'art':'NOT_ADOPTED',
   'G0':'NOT_RUN','formal_S1_G1_G2_G3':'NOT_RUN','minecraft':'FORBIDDEN',
   'limitations':['Visual scope is one inhabited section, not entire city',
     'No 2 operating lifts or emergency staircases',
     'No enclosed certified dwellings',
     'No structural load simulations',
     'No formal width-swept 331/993 QA',
     'No MakeCode compilation or construction']}
 (folder/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
 (folder/'program.json').write_text(json.dumps(program,indent=2,ensure_ascii=False))
 print(folder.name,'faces',len(full.faces),'program',len(program),'bounds',full.bounds.tolist(),flush=True)
 return manifest
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--case',type=int,choices=[70,90],default=70);ap.add_argument('--no-research',action='store_true');a=ap.parse_args();build(a.case,not a.no_research)