"""G4-C7 B11-R5 D7: program-to-form authored 3D study.
Research prototype, not architecture, safety, or Minecraft construction.
All mesh outputs are direct from this source. Requires numpy and trimesh.
"""
from pathlib import Path
import json, hashlib, math
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
COLORS={
 'ground':(67,80,92,255), 'fabrication':(221,161,109,255),
 'civic':(236,209,150,255), 'skeleton':(104,142,173,255),
 'canopy':(178,201,213,255), 'gallery':(87,207,203,255),
 'research':(139,164,229,255), 'habitat':(226,222,184,255),
 'glazing':(126,229,227,145),'core':(91,144,182,255),
 'machine':(229,111,91,255), 'green':(116,174,117,255)
}
PARTS={k:[] for k in COLORS}


def reset():
 for k in PARTS:PARTS[k]=[]

def add(mesh,group):
 mesh.visual.vertex_colors=np.tile(COLORS[group],(len(mesh.vertices),1)); PARTS[group].append(mesh)

def box(cx,cy,z,dx,dy,h,group,rot=0):
 m=trimesh.creation.box(extents=[dx,dy,h]);m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(rot),[0,0,1]));m.apply_translation([cx,cy,z+h/2]);add(m,group)

def tube(path,r,group,sections=10):
 for a,b in zip(path,path[1:]):
  if np.linalg.norm(np.subtract(b,a))<.01:continue
  add(trimesh.creation.cylinder(radius=r,segment=[a,b],sections=sections),group)

def loft(path,widths,depths,group,up=None):
 """Continuous variable-width/depth solid along an authored spatial axis.
 Width direction is horizontal perpendicular to the XY tangent. It is a beam,
 not an unbounded vertical façade and not a repeating circular ring.
 """
 p=np.array(path,dtype=float);v=[]
 for i,c in enumerate(p):
  direction=p[min(i+1,len(p)-1)]-p[max(i-1,0)]; direction[2]=0
  length=np.linalg.norm(direction);assert length>0
  u=np.array([-direction[1],direction[0],0])/length
  w=widths[i]*.5;d=depths[i]*.5
  v.extend([c+u*w+[0,0,d],c-u*w+[0,0,d],c+u*w-[0,0,d],c-u*w-[0,0,d]])
 faces=[]
 for i in range(len(p)-1):
  a=4*i;b=a+4
  for x,y,x2,y2 in [(0,1,0,1),(2,3,2,3),(0,2,0,2),(1,3,1,3)]:
   # preserve two triangles, cross section quad between stations
   faces.extend([[a+x,b+x2,b+y2],[a+x,b+y2,a+y]])
 faces.extend([[0,1,3],[0,3,2]])
 b=len(v)-4;faces.extend([[b,b+3,b+1],[b,b+2,b+3]])
 m=trimesh.Trimesh(vertices=np.array(v),faces=np.array(faces),process=False)
 add(m,group)

def ribbon(path,width,thick,group):
 # call loft with axis at deck top - thickness/2 and depth thickness
 p=np.array(path,float);p[:,2]-=thick*.5
 loft(p,[width]*len(p),[thick]*len(p),group)

def program(clearance):
 return {
  'fabrication_floor_z':18.0,
  'fabrication_open_height':clearance,
  'public_axis_z':23.5,
  'studio_stage_xy':[-68,-22],
  'research_public_z':112,
  'research_open_air_z':142,
  'residential_terrace_z':195,
  'two_lifts_ground_z':18,
  'art_state':'NOT_ADOPTED',
 }

def build(clearance=70, include_research=True):
 assert clearance in (70,90)
 reset();cfg=program(clearance)
 floor=cfg['fabrication_floor_z'];roof=floor+clearance
 # Ground is a clipped landscape, not full rectangular city foundation.
 box(-65,-58,12,284,225,9,'ground',rot=-8)
 box(95,120,13,195,129,12,'ground',rot=21)
 # Real fab floor / loading zone, bounded clear height roof test.
 box(-64,-61,18,196,118,3,'fabrication',rot=-10)
 box(-70,-20,21,72,55,3,'machine',rot=-10)
 for x,y in [(-100,-36),(-84,-20),(-53,-12),(-34,-30)]:
  box(x,y,24,8,7,5,'machine',rot=22)
 tube([[-105,-21,30],[-93,-17,46],[-40,-12,46],[-25,-20,30]],1.4,'skeleton')
 # Public ground promenade / learning steps, actual physical deck; no human route cert.
 ribbon([[-192,67,23.5],[-125,64,23.5],[-52,75,23.5],[12,86,23.5],[94,102,23.5],[174,118,23.5]],12,2.4,'civic')
 ribbon([[-125,64,23.5],[-107,34,24.1],[-90,12,24.8]],8,1.8,'gallery')
 box(-95,10,24,22,13,1.4,'gallery',rot=-13)
 # Research activity is embedded in upper arch width; an inhabitable open deck at 112m.
 # 3 sculptural multi-arch spines are anchored by activity heights, not from surface repeats.
 # First arch: forms fabrication roof clearance and public gallery anchorage.
 spineA=[[-168,-100,23],[-157,-77,54],[-132,-60,roof-4],[-93,-37,roof+25],[-48,-7,roof+39],[-8,31,roof+31],[50,64,roof+16],[98,91,74]]
 loft(spineA,[13,20,26,38,38,31,21,18],[14,18,23,24,20,19,16,17],'skeleton')
 spineB=[[163,-81,22],[131,-75,59],[96,-50,roof+5],[67,-12,roof+43],[37,31,roof+72],[31,82,145],[56,140,183],[119,182,196]]
 loft(spineB,[14,17,25,36,42,36,27,21],[15,21,26,30,26,19,18,17],'skeleton')
 # Programmatic roof concave segment: only above workshop; not giant opaque wall.
 # Transverse vault scales if fabrication clearance changes, housing stays fixed.
 loft([[-139,-101,roof+8],[-102,-89,roof+12],[-65,-69,roof+16],[-30,-31,roof+13],[15,18,roof+9],[40,60,roof+4]],
      [33,46,66,72,45,18],[8,10,12,12,9,7],'canopy')
 # True volume-free skylight remains between diagonal vault rib bundles, no cap across canyon.
 # Third oblique shared structural anchor to tall public research terraces.
 spineC=[[-191,60,18],[-164,74,48],[-123,82,88],[-93,112,116],[-70,146,146],[-37,174,185],[12,184,220],[67,208,231]]
 loft(spineC,[18,25,29,29,31,35,31,23],[17,19,20,22,23,23,19,16],'skeleton')
 # Observational platform folds together with rib B's public transition.
 ribbon([[-132,-36,roof-22],[-96,-18,roof-15],[-57,5,roof+3],[-11,27,roof+24],[20,45,roof+41]],10,2.4,'gallery')
 # Upper research public deck and cultural open theatre = genuinely thick floor.
 if include_research:
  ribbon([[-85,125,112],[-48,130,112],[-6,141,112],[35,156,112],[83,174,112]],22,3.2,'research')
  # open lecture/experiment stage and several vertical view markers
  box(5,138,112,25,17,3.2,'research',rot=18)
  box(4,132,115.2,8,5,3,'machine',rot=18)
  for x,y in [(-43,127),(-21,132),(22,149),(63,167)]:box(x,y,112,7,4,1,'civic',rot=20)
  # an authentic three-sided low height enclosure; deliberately an open public lab
  box(-20,169,112,57,6,15,'research',rot=19)
  box(-53,151,112,5,39,15,'research',rot=18)
  box(18,153,112,5,28,15,'research',rot=18)
  # difference between removal and addition changes structural outboard arch geometry
  loft([[-85,125,112],[-76,160,132],[-31,174,161],[29,180,178],[78,184,174]],
       [15,25,28,23,16],[15,17,22,18,13],'skeleton')
  # Light aperture / tall civic learning terrace within inhabited structure
  ribbon([[-38,176,141],[6,181,143],[53,183,146]],18,2,'research')
  for x,y in [(-14,179),(32,183)]:box(x,y,146,10,6,2,'green')
 # Demonstrable two vertical cores as UNBUILT lift volumes; frames + stations only.
 for x,y,zmax in [(-170,78,201),(101,116,201)]:
  for dx in (-8,8):
   for dy in (-8,8):tube([[x+dx,y+dy,18],[x+dx,y+dy,zmax]],.75,'core')
  for z in (23.5,112,195): box(x,y,z,16,16,1.5,'core')
 # Outer residence: outdoor public elevated terrace plus 2 actually enclosed test cells.
 # Connectedness is UNRESOLVED; no false inhabited district or safe exit.
 ribbon([[-12,158,195],[23,174,195],[58,192,195],[92,203,195]],19,3.8,'habitat')
 for x,y in [(19,184),(62,203)]:
  # Private two-sided pods under sculptural spines. NOT certified rooms.
  box(x,y,195,18,16,2.4,'habitat',rot=25)
  box(x-9,y,197.4,1.3,16,9,'habitat',rot=25)
  box(x+9,y,197.4,1.3,16,9,'habitat',rot=25)
  box(x,y+8,197.4,18,1.2,9,'glazing',rot=25)
  box(x,y,206.4,18,16,2,'habitat',rot=25)
 # Upper civic anchor is not a whole-city skyline.
 tube([[95,182,195],[112,193,235],[134,208,257]],3,'skeleton')
 # Detail: public use visible as vertical circulation ribs and optical portals;
 # avoid inventing functioning lifts, accessibility, egress or structural engineering.
 folder=ROOT/(f'clearance_{clearance}' + ('_no_research' if not include_research else ''))
 folder.mkdir(parents=True,exist_ok=True)
 combined=[]
 for name,meshes in PARTS.items():
  if meshes:
   m=trimesh.util.concatenate(meshes);m.export(folder/(name+'.ply'));combined.append(m)
 full=trimesh.util.concatenate(combined);full.export(folder/'model.obj')
 scene=trimesh.Scene()
 for name,meshes in PARTS.items():
  if meshes:scene.add_geometry(trimesh.util.concatenate(meshes),geom_name=name)
 scene.export(folder/'model.glb')
 meta={'stage':'B11-R5 D7','local_only':True,'clearance_input_m':clearance,'research_program':include_research,
       'parts':list(COLORS),'faces':len(full.faces),'vertices':len(full.vertices),'bounds_m':full.bounds.tolist(),
       'obj_sha256':hashlib.sha256((folder/'model.obj').read_bytes()).hexdigest(),
       'glb_sha256':hashlib.sha256((folder/'model.glb').read_bytes()).hexdigest(),
       'design_program':cfg,'formal_qa':'NOT_RUN','G0':'NOT_ADOPTED','minecraft':'FORBIDDEN',
       'limitations':['not a complete city','arches not load engineered','no rooms certified','cores frame-only, no lifts',
          'no safe stairs/egress','ribbons not certified walkable','point roof clearance requires mesh verification','MakeCode only research, not built']}
 (folder/'manifest.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False),encoding='utf8')
 return folder,meta

if __name__=='__main__':
 for h in (70,90):
  path,m=build(h);print('BUILT',path,m['faces'],m['bounds_m'],flush=True)
 path,m=build(70,False);print('NEGATIVE CONTROL RESEARCH REMOVED',m['faces'],flush=True)
